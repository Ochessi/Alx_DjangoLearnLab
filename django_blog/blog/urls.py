from django.urls import path
from .views import PostListView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
