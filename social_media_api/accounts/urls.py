from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),                # current authenticated user
    path('profile/<str:username>/', UserDetailView.as_view(), name='profile-detail'),  # public
]
