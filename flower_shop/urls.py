from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from flowershop_bot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('quiz/', views.quiz_view, name='quiz_page'),
    path('quiz-step/<str:occasion>/', views.quiz_step_view, name='quiz_step'),
    path('result/<str:price>/', views.result, name='result'),
    path('order/<int:bouquet_id>/', views.order_view, name='order'),
    path('order-step/<int:bouquet_id>/', views.order_step, name='order_step'),
    path('payment_confirmation/<int:pk>/', views.payment_confirmation, name='payment_confirmation'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    path('payment_failed/', views.payment_failed_view, name='payment_failed'),
    path('consultation/', views.consultation_page, name='consultation_page'),
    path('card/<int:bouquet_id>/', views.card_page, name='card_page'),
    path('load_more_bouquets/', views.load_more_bouquets, name='load_more_bouquets'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
