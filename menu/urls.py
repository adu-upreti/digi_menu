# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Public menu display
    path('<slug:restaurant_slug>-menu/', views.restaurant_menu_view, name='restaurant_menu'),
]