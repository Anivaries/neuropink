from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('order/', views.order_view, name='order'),
    path('order-50/', views.order_view_fifty_grams, name='order-fifty'),
    # path('order/<int:order_number>', views.order_success, name='order_success'),
    path("order/<uuid:token>/", views.order_success, name="order_success"),
    path('testimonial/', views.testimonial_success, name='testimonial_success'),
    path('load-more/', views.load_more_testimonials,
         name='load_more_testimonials'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
