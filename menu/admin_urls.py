from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('share/', views.menu_share_view, name='menu_share'),
    path('qr-download/', views.generate_qr_code, name='generate_qr_code'),
    path('qr-image/', views.get_qr_code_image, name='get_qr_code_image'),
]