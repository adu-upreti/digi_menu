from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

def home(request):
    return render(request, 'user/index.html')

def how_it_works(request):
    return render(request, 'user/how-it-works.html')

def signup(request):
    if request.method == 'POST':
        # Check if it's login or register based on which form was submitted
        if 'email' in request.POST and 'registerEmail' not in request.POST:
            # This is a login request
            return login_user(request)
        elif 'registerEmail' in request.POST:
            # This is a register request
            return register_user(request)
    
    return render(request, 'user/signup.html')

def login_user(request):
    try:
        # Get data from POST request
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email (since Django uses username by default)
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'user/signup.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to admin dashboard (assuming it's in admin_panel app)
            return redirect('dashboard')  # Adjust this path according to your admin_panel URLs
        else:
            messages.error(request, 'Invalid email or password.')
            
    except Exception as e:
        messages.error(request, 'An error occurred during login. Please try again.')
    
    return render(request, 'user/signup.html')

def register_user(request):
    try:
        # Get data from POST request
        restaurant_name = request.POST.get('restaurantName')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')
        terms = request.POST.get('terms')
        
        # Validation
        if not all([restaurant_name, phone_number, email, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'user/signup.html')
        
        if not terms:
            messages.error(request, 'You must agree to the Terms of Service.')
            return render(request, 'user/signup.html')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'user/signup.html')
        
        # Create user (using email as username)
        user = User.objects.create_user(
            username=email,  # Using email as username
            email=email,
            password=password,
            first_name=restaurant_name  # Store restaurant name in first_name field
        )
        
        # You can create a profile model later to store phone_number
        # For now, we'll store it in last_name field (temporary solution)
        user.last_name = phone_number
        user.save()
        
        messages.success(request, 'Account created successfully! Please log in.')
        return render(request, 'user/signup.html')
        
    except Exception as e:
        messages.error(request, 'An error occurred during registration. Please try again.')
    
    return render(request, 'user/signup.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('signup')  # Redirect to login page

# Remove this dashboard function since it's in admin_panel app