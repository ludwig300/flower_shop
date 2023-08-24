import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from dotenv import load_dotenv
from yookassa import Configuration

from .models import Bouquet, Order, Quiz
from .payments import create_payment, get_payment_status

load_dotenv()

Configuration.shop_id = os.getenv('YOOKASSA_SHOP_ID')
Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')


def payment_confirmation(request, pk):
    order = Order.objects.get(id=pk)
    status = get_payment_status(order.payment_id)

    if status == 'succeeded':
        order = Order.objects.get(payment_id=order.payment_id)
        order.is_paid = True
        order.save()
        context = {'pk': pk}
        return render(request, 'payment_success.html', context)
    else:
        return render(request, 'payment_failed.html')


def payment_success_view(request):
    return render(request, 'payment_success.html')


def payment_failed_view(request):
    return render(request, 'payment_failed.html')


def index(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'index.html', {'bouquets': bouquets})


def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'catalog.html', {'bouquets': bouquets})


def quiz_view(request):
    return render(request, 'quiz.html')


def quiz_step_view(request, occasion):
    request.session['occasion'] = occasion
    return render(request, 'quiz-step.html', {'occasion': occasion})


def result(request, price):
    occasion = request.session.get('occasion', 'no_occasion')
    quiz = Quiz.objects.filter(occasion=occasion, price_range=price).first()
    bouquets = quiz.bouquets.all() if quiz else []
    return render(request, 'result.html', {'bouquets': bouquets})


def order_view(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    context = {'bouquet': bouquet}
    return render(request, 'order.html', context)


def consultation_page(request):
    return render(request, 'consultation.html')


def card_page(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    context = {'bouquet': bouquet}
    return render(request, 'card.html', context)


def load_more_bouquets(request):
    offset = int(request.GET.get('offset', 3))
    limit = int(request.GET.get('limit', 3))
    bouquets = Bouquet.objects.all()[offset:offset + limit]
    bouquet_list = list(bouquets.values('id', 'name', 'price'))
    return JsonResponse(bouquet_list, safe=False)


def quiz_step(request, occasion):
    quiz = Quiz.objects.filter(occasion=occasion).first()
    bouquets = quiz.bouquets.all() if quiz else []
    return render(request, 'quiz_step.html', {'bouquets': bouquets})


def order_step(request, bouquet_id):
    if request.method == 'POST':
        customer_name = request.POST.get('fname')
        customer_phone = request.POST.get('tel')
        delivery_address = request.POST.get('adres')
        delivery_time = request.POST.get('orderTime')

        bouquet = Bouquet.objects.get(pk=bouquet_id)

        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            bouquet=bouquet
        )
        description = f"Описание заказа №{order.id}"
        amount = bouquet.price
        return_url = request.build_absolute_uri(reverse('payment_confirmation', kwargs={'pk': order.pk}))

        payment = create_payment(order.id, amount, description, return_url)
        order.payment_id = payment.id
        order.save()

        return redirect(payment.confirmation.confirmation_url)
    else:
        return render(request, 'order_step.html')
