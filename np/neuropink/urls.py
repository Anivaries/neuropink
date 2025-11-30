from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('order/', views.order_view, name='order'),
    path('order/<int:order_number>', views.order_success, name='order_success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
