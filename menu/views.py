# menu/views.py
from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category, MenuItem
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
import os


def restaurant_menu_view(request, restaurant_slug):
    """
    Public view to display a restaurant's menu
    """
    # Get restaurant or 404
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    
    # Get categories and menu items for this restaurant
    categories = Category.objects.filter(restaurant=restaurant).order_by('name')
    menu_items = MenuItem.objects.filter(
        restaurant=restaurant, 
        is_available=True  # Only show available items
    ).order_by('category__name', 'name')
    
    # Get featured items for banner/carousel
    featured_items = MenuItem.objects.filter(
        restaurant=restaurant, 
        is_featured=True, 
        is_available=True
    )[:5]  # Limit to 5 featured items
    
    # Optional: Structure menu items by category for easier template rendering
    categorized_menu = {}
    for category in categories:
        categorized_menu[category.name] = menu_items.filter(category=category)
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
        'menu_items': menu_items,
        'featured_items': featured_items,
        'categorized_menu': categorized_menu,
    }
    return render(request, 'admin/menu-template.html', context)


@login_required
def menu_share_view(request):
    try:
        restaurant = request.user.restaurant_profile
        
        # Build the full menu URL
        menu_url = request.build_absolute_uri(f'/{restaurant.slug}-menu/')
        
        context = {
            'restaurant': restaurant,
            'menu_url': menu_url,
        }
        return render(request, 'admin/menu-share.html', context)
        
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant profile not found.')
        return redirect('dashboard')

@login_required
def generate_qr_code(request):
    try:
        restaurant = request.user.restaurant_profile
        
        # Build the full menu URL
        menu_url = request.build_absolute_uri(f'/{restaurant.slug}-menu/')
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(menu_url)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Create HTTP response with download
        response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{restaurant.slug}-menu-qr.png"'
        
        return response
        
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant profile not found.')
        return redirect('dashboard')

@login_required
def get_qr_code_image(request):
    """Generate QR code for display (not download)"""
    try:
        restaurant = request.user.restaurant_profile
        menu_url = request.build_absolute_uri(f'/{restaurant.slug}-menu/')
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(menu_url)
        qr.make(fit=True)
        
        # Create image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Return as HTTP response for display
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
        return response
        
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant not found", status=404)