from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('menu-management/', views.menu_management, name='menu_management'),
    path('category-management/', views.category_management, name='category_management'),
    path('reviews/', views.reviews, name='reviews'),
]