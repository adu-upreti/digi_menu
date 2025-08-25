from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('global.urls')),
    path('', include('admin_panel.urls')),
    path('', include('global.urls')),
]
