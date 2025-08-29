# menu/admin.py
from django.contrib import admin
from .models import Restaurant, Category, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'slug', 'user__username')
    prepopulated_fields = {'slug': ('name',)} # This helps in admin, but our save() method handles uniqueness

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_available', 'is_featured', 'is_special')
    list_filter = ('restaurant', 'category', 'is_available', 'is_featured', 'is_special')
    search_fields = ('name', 'description', 'restaurant__name')
    raw_id_fields = ('restaurant', 'category') # Useful for large number of restaurants/categories