from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('order/', views.order_view, name='order'),
    path('order/<int:order_number>', views.order_success, name='order_success'),
]
