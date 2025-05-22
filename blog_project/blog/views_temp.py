from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Post
from .models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post
from django.urls import reverse

@login_required
def message_board(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'blog/message_board.html', {'messages': messages})

@login_required
def post_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(user=request.user, content=content)
        return redirect('message_board')
    return render(request, 'blog/post_message.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse('message_board')
