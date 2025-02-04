from django.contrib.auth import views as auth_views  # <-- ADD THIS
from django.urls import path, include
from . import views  # Import your app's views
urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    # Include password reset URLs if needed (optional)
    path('', include('django.contrib.auth.urls')),
]