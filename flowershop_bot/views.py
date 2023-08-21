from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Bouquet


def index(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'index.html', {'bouquets': bouquets})


def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'catalog.html', {'bouquets': bouquets})


def quiz_view(request):
    return render(request, 'quiz.html')


def quiz_step_view(request, occasion):
    return render(request, 'quiz-step.html', {'occasion': occasion})


def result_view(request, price):
    if price == 'under-1000':
        bouquets = Bouquet.objects.filter(price__lt=1000)
    elif price == '1000-5000':
        bouquets = Bouquet.objects.filter(price__gte=1000, price__lte=5000)
    elif price == 'over-5000':
        bouquets = Bouquet.objects.filter(price__gt=5000)
    elif price == 'no-matter':
        bouquets = Bouquet.objects.all()
    else:
        bouquets = []

    context = {
        'bouquets': bouquets,
    }

    return render(request, 'result.html', context)


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
    bouquet_list = list(bouquets.values('id', 'name', 'price')) # Можно добавить другие поля
    return JsonResponse(bouquet_list, safe=False)