# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Public menu display
    path('<slug:restaurant_slug>-menu/', views.restaurant_menu_view, name='restaurant_menu'),
    
    # Menu sharing page (IMPORTANT: This should be BEFORE the slug pattern)
    path('share/', views.menu_share_view, name='menu_share'),
    
    # QR code generation
    path('qr-download/', views.generate_qr_code, name='generate_qr_code'),
    path('qr-image/', views.get_qr_code_image, name='get_qr_code_image'),
]
