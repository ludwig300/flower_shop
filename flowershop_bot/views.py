from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Bouquet, Quiz


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


def order_view(request):
    return render(request, 'order.html')


def order_step_view(request):
    return render(request, 'order-step.html')


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
