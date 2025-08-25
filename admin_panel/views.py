from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'admin/admin.html', {
        'user': request.user
    })

def menu_management(request):
    return render(request, 'admin/menu-management.html')

def category_management(request):
    return render(request, 'admin/category-management.html')

def reviews(request):
    return render(request, 'admin/reviews.html')
