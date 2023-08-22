from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from flowershop_bot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('quiz/', views.quiz_view, name='quiz_page'),
    path('quiz-step/<str:occasion>/', views.quiz_step_view, name='quiz_step'),
    path('result/<str:price>/', views.result, name='result'),
    path('order/', views.order_view, name='order'),
    path('order-step/', views.order_step_view, name='order_step'),
    path('consultation/', views.consultation_page, name='consultation_page'),
    path('card/<int:bouquet_id>/', views.card_page, name='card_page'),
    path('load_more_bouquets/', views.load_more_bouquets, name='load_more_bouquets'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
