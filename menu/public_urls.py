from django.urls import path
from . import views

urlpatterns = [
    path('<slug:restaurant_slug>-menu/', views.restaurant_menu_view, name='restaurant_menu'),
]