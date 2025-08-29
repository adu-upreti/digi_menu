# menu/views.py
from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category, MenuItem

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