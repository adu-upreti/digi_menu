from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from menu.models import Restaurant, Category, MenuItem

@login_required
def dashboard(request):
    try:
        # Get the restaurant profile for the logged-in user
        restaurant = request.user.restaurant_profile  # Using the related_name from models
        
        # Get some basic stats for the dashboard
        total_categories = Category.objects.filter(restaurant=restaurant).count()
        total_menu_items = MenuItem.objects.filter(restaurant=restaurant).count()
        available_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True).count()
        featured_items = MenuItem.objects.filter(restaurant=restaurant, is_featured=True).count()
        
        context = {
            'user': request.user,
            'restaurant': restaurant,
            'total_categories': total_categories,
            'total_menu_items': total_menu_items,
            'available_items': available_items,
            'featured_items': featured_items,
            'menu_url': f"/{restaurant.slug}-menu/",  # The public menu URL
        }
        return render(request, 'admin/admin.html', context)
        
    except Restaurant.DoesNotExist:
        # Handle case where user doesn't have a restaurant profile
        messages.error(request, 'Restaurant profile not found. Please contact support.')
        return redirect('signup')

@login_required
def menu_management(request):
    try:
        restaurant = request.user.restaurant_profile
        
        # Handle form submission (Create/Update)
        if request.method == 'POST':
            item_name = request.POST.get('itemName')
            item_category = request.POST.get('itemCategory')
            item_price = request.POST.get('itemPrice')
            item_description = request.POST.get('itemDescription', '')
            item_image = request.FILES.get('itemImage')
            is_available = request.POST.get('isAvailable') == 'on'
            is_featured = request.POST.get('isFeatured') == 'on'
            is_special = request.POST.get('isSpecial') == 'on'
            item_id = request.POST.get('item_id')  # For edit mode
            
            if not all([item_name, item_price]):
                messages.error(request, 'Item name and price are required.')
            else:
                try:
                    # Get category object if provided
                    category_obj = None
                    if item_category:
                        category_obj = get_object_or_404(Category, id=item_category, restaurant=restaurant)
                    
                    if item_id:  # Edit existing item
                        menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
                        menu_item.name = item_name
                        menu_item.category = category_obj
                        menu_item.price = float(item_price)
                        menu_item.description = item_description
                        menu_item.is_available = is_available
                        menu_item.is_featured = is_featured
                        menu_item.is_special = is_special
                        
                        # Update image only if new one is provided
                        if item_image:
                            menu_item.image = item_image
                        
                        menu_item.save()
                        messages.success(request, f'Menu item "{item_name}" updated successfully!')
                    else:  # Create new item
                        MenuItem.objects.create(
                            restaurant=restaurant,
                            category=category_obj,
                            name=item_name,
                            price=float(item_price),
                            description=item_description,
                            image=item_image,
                            is_available=is_available,
                            is_featured=is_featured,
                            is_special=is_special
                        )
                        messages.success(request, f'Menu item "{item_name}" created successfully!')
                        
                except ValueError:
                    messages.error(request, 'Please enter a valid price.')
                except Exception as e:
                    messages.error(request, f'Error saving menu item: {str(e)}')
            
            return redirect('menu_management')
        
        # Get data for display
        menu_items = MenuItem.objects.filter(restaurant=restaurant).order_by('category__name', 'name')
        categories = Category.objects.filter(restaurant=restaurant).order_by('name')
        
        context = {
            'restaurant': restaurant,
            'menu_items': menu_items,
            'categories': categories,
        }
        return render(request, 'admin/menu-management.html', context)
        
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant profile not found.')
        return redirect('dashboard')

# Add this new function for AJAX delete
@login_required
@require_POST
@csrf_exempt
def delete_menu_item_ajax(request):
    try:
        restaurant = request.user.restaurant_profile
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
        item_name = menu_item.name
        menu_item.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Menu item "{item_name}" deleted successfully!'
        })
        
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Restaurant profile not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error deleting menu item: {str(e)}'})


@login_required
def category_management(request):
    try:
        restaurant = request.user.restaurant_profile
        
        # Handle form submission (Create/Update)
        if request.method == 'POST':
            category_name = request.POST.get('categoryName')
            category_description = request.POST.get('categoryDescription', '')
            category_id = request.POST.get('category_id')  # For edit mode
            
            if not category_name:
                messages.error(request, 'Category name is required.')
            else:
                try:
                    if category_id:  # Edit existing category
                        category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
                        category.name = category_name
                        category.description = category_description
                        category.save()
                        messages.success(request, f'Category "{category_name}" updated successfully!')
                    else:  # Create new category
                        # Check if category already exists for this restaurant
                        if Category.objects.filter(restaurant=restaurant, name=category_name).exists():
                            messages.error(request, f'Category "{category_name}" already exists.')
                        else:
                            Category.objects.create(
                                restaurant=restaurant,
                                name=category_name,
                                description=category_description
                            )
                            messages.success(request, f'Category "{category_name}" created successfully!')
                except Exception as e:
                    messages.error(request, f'Error saving category: {str(e)}')
            
            return redirect('category_management')
        
        # Get all categories for this restaurant with item counts
        categories = Category.objects.filter(restaurant=restaurant).order_by('name')
        categories_with_counts = []
        
        for category in categories:
            item_count = MenuItem.objects.filter(category=category).count()
            categories_with_counts.append({
                'category': category,
                'item_count': item_count
            })
        
        # Get stats for analytics cards
        total_categories = categories.count()
        total_menu_items = MenuItem.objects.filter(restaurant=restaurant).count()
        available_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True).count()
        featured_items = MenuItem.objects.filter(restaurant=restaurant, is_featured=True).count()
        
        context = {
            'restaurant': restaurant,
            'categories_with_counts': categories_with_counts,
            'total_categories': total_categories,
            'total_menu_items': total_menu_items,
            'available_items': available_items,
            'featured_items': featured_items,
        }
        return render(request, 'admin/category-management.html', context)
        
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant profile not found.')
        return redirect('dashboard')


@login_required
@require_POST
@csrf_exempt
def delete_category_ajax(request):
    try:
        restaurant = request.user.restaurant_profile
        data = json.loads(request.body)
        category_id = data.get('category_id')
        
        category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
        
        # Check if category has menu items
        item_count = MenuItem.objects.filter(category=category).count()
        if item_count > 0:
            return JsonResponse({
                'success': False, 
                'message': f'Cannot delete category "{category.name}" because it contains {item_count} menu items. Please move or delete the items first.'
            })
        
        category_name = category.name
        category.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Category "{category_name}" deleted successfully!'
        })
        
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Restaurant profile not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error deleting category: {str(e)}'})


def reviews(request):
    return render(request, 'admin/reviews.html')

