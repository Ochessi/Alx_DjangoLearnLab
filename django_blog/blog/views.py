from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from .models import Post

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Your account has been created!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')
    return render(request, 'blog/profile.html')    
