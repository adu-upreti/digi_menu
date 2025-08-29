from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model
from django.utils.text import slugify # For generating URL-friendly slugs
from PIL import Image # Required for image processing (Pillow library)

# 1. Restaurant Model
class Restaurant(models.Model):
    """
    Represents a single restaurant registered on DigiMenu.
    Each restaurant is linked to a unique user account.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='restaurant_profile', # Custom related_name for reverse lookup
        help_text="The user account associated with this restaurant."
    )
    name = models.CharField(
        max_length=255,
        unique=False, # Restaurant names can be duplicated, slugs handle uniqueness
        help_text="The display name of the restaurant (e.g., 'Vrindavan Sweets')."
    )
    slug = models.SlugField(
        max_length=255,
        unique=True, # Ensures the URL part is unique
        blank=True, # Allows the field to be blank initially
        help_text="Unique URL-friendly identifier for the restaurant's menu page."
    )
    logo = models.ImageField(
        upload_to='restaurant_logos/',
        blank=True,
        null=True,
        help_text="Upload the restaurant's logo image."
    )
    contact_info = models.TextField(
        blank=True,
        null=True,
        help_text="Contact details for the restaurant (e.g., address, phone)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the restaurant profile was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the restaurant profile was last updated."
    )

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ['name'] # Default ordering for querysets

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a unique slug
        before saving the Restaurant instance.
        """
        if not self.slug: # Only generate slug if it's not already set
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            # Check if a restaurant with this slug already exists
            # Exclude the current instance if it's an update
            while Restaurant.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

        # Optional: Resize logo after saving if it's too large
        if self.logo:
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300: # Example: Resize if larger than 300x300
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path)


# 2. Category Model
class Category(models.Model):
    """
    Represents a menu category within a specific restaurant (e.g., Appetizers, Main Course).
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories', # Allows restaurant.categories.all()
        help_text="The restaurant this category belongs to."
    )
    name = models.CharField(
        max_length=100,
        help_text="Name of the menu category (e.g., 'Appetizers', 'Desserts')."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description for the category."
    )
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ('restaurant', 'name') # A restaurant cannot have two categories with the same name
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


# 3. MenuItem Model
class MenuItem(models.Model):
    """
    Represents an individual food or beverage item on a restaurant's menu.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items', # Allows restaurant.menu_items.all()
        help_text="The restaurant this menu item belongs to."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # If a category is deleted, items become uncategorized (category=NULL)
        related_name='items', # Allows category.items.all()
        blank=True,
        null=True,
        help_text="The category this menu item belongs to (optional)."
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the menu item (e.g., 'Paneer Butter Masala')."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="A short description of the menu item."
    )
    price = models.DecimalField(
        max_digits=10, # Max 99,999,999.99
        decimal_places=2,
        help_text="Price of the menu item."
    )
    image = models.ImageField(
        upload_to='menu_items/',
        blank=True,
        null=True,
        help_text="Upload an image for the menu item."
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Check if the item is currently available."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Check to mark this item as featured (e.g., for a carousel)."
    )
    is_special = models.BooleanField(
        default=False,
        help_text="Check to mark this item as a 'Today's Special'."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the menu item was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the menu item was last updated."
    )

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['category__name', 'name'] # Order by category then by item name

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Optional: Resize image after saving if it's too large
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600: # Example: Resize if larger than 600x600
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)
