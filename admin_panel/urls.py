from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('menu-management/', views.menu_management, name='menu_management'),
    path('category-management/', views.category_management, name='category_management'),
    path('reviews/', views.reviews, name='reviews'),
    path('delete-category-ajax/', views.delete_category_ajax, name='delete_category_ajax'),
    path('delete-menu-item-ajax/', views.delete_menu_item_ajax, name='delete_menu_item_ajax'),
]