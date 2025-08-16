from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from .models import Post, Comment
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.db.models import Q

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

# List all posts (open to everyone)
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ['-published_date']

# View a single post (open to everyone)
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.select_related('author')
        ctx['comment_form'] = CommentForm()
        return ctx
# Create a post (logged-in users only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Edit a post (only the author can)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post (only the author can)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Create a comment (logged-in users only)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted.")
        else:
            messages.error(request, "Could not post comment. Please fix the errors.")
        return redirect(post.get_absolute_url())

# Edit a comment (only the author)
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        messages.success(self.request, "Comment updated.")
        return self.object.post.get_absolute_url()

# Delete a comment (only the author)
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        messages.success(self.request, "Comment deleted.")
        return self.object.post.get_absolute_url()   

def search_posts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})    

def posts_by_tag(request, tag_name):
    posts = Post.objects.filter(tags__name__iexact=tag_name)
    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag': tag_name})

