from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Post, Message, Blog
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LogoutView, LoginView
from .forms import BlogForm, UserProfileForm, UserEmailForm, MessageForm
from django.core.paginator import Paginator
from collections import defaultdict

@login_required
def message_board(request):
    messages = Message.objects.filter(post__isnull=True, blog__isnull=True).order_by('-created_at')
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

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    messages = Message.objects.filter(post=post).order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'messages': messages})

@login_required
def profile(request):
    from .models import UserProfile
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        email_form = UserEmailForm(request.POST, instance=user)
        if profile_form.is_valid() and email_form.is_valid():
            profile_form.save()
            email_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        email_form = UserEmailForm(instance=user)
    return render(request, 'blog/profile.html', {
        'profile_form': profile_form,
        'email_form': email_form,
        'user_profile': user_profile,
    })

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    http_method_names = ['get', 'post']

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse('message_board')

from django.http import HttpResponseForbidden

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Allow deletion if user is message owner or blog owner
    if message.user != request.user:
        if message.blog is None or message.blog.user != request.user:
            return HttpResponseForbidden("You are not allowed to delete this message.")
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('message_board')
    return render(request, 'blog/confirm_delete_message.html', {'message': message})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog created successfully.')
            return redirect('user_blogs', user_id=request.user.id)
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required
def user_blogs(request, user_id):
    blogs = Blog.objects.filter(user__id=user_id)
    blog_id = request.GET.get('blog_id')
    selected_blog = None
    posts = []
    post_messages = defaultdict(list)
    blog_messages = []
    message_form = MessageForm()

    if blog_id:
        selected_blog = get_object_or_404(Blog, id=blog_id, user__id=user_id)
        posts = selected_blog.posts.all()
        messages = Message.objects.filter(post__in=posts).order_by('-created_at')
        for message in messages:
            post_messages[message.post.id].append(message)

        blog_messages = Message.objects.filter(blog=selected_blog).order_by('-created_at')

        # Optional: paginate posts if needed
        paginator = Paginator(posts, 10)  # 10 posts per page
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

    context = {
        'blogs': blogs,
        'selected_blog': selected_blog,
        'posts': posts,
        'post_messages': post_messages,
        'blog_messages': blog_messages,
        'message_form': message_form,
    }
    return render(request, 'blog/user_blog.html', context)

@login_required
def post_message_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content, post=post)
            # Instead of redirect, render user_blog.html with updated context
            user_id = request.user.id
            blogs = Blog.objects.filter(user__id=user_id)
            selected_blog = None
            posts = []
            post_messages = defaultdict(list)
            blog_messages = []
            message_form = MessageForm()

            # Find the blog that contains this post
            for blog in blogs:
                if post in blog.posts.all():
                    selected_blog = blog
                    break

            if selected_blog:
                posts = selected_blog.posts.all()
                messages_qs = Message.objects.filter(post__in=posts).order_by('-created_at')
                for message in messages_qs:
                    post_messages[message.post.id].append(message)
                blog_messages = Message.objects.filter(blog=selected_blog).order_by('-created_at')
                paginator = Paginator(posts, 10)
                page_number = request.GET.get('page')
                posts = paginator.get_page(page_number)

            context = {
                'blogs': blogs,
                'selected_blog': selected_blog,
                'posts': posts,
                'post_messages': post_messages,
                'blog_messages': blog_messages,
                'message_form': message_form,
            }
            return render(request, 'blog/user_blog.html', context)
    return render(request, 'blog/post_message.html', {'post': post})

@login_required
def post_message_on_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content, blog=blog)
            # Instead of redirect, render user_blog.html with updated context
            user_id = request.user.id
            blogs = Blog.objects.filter(user__id=user_id)
            selected_blog = blog
            posts = selected_blog.posts.all()
            post_messages = defaultdict(list)
            blog_messages = Message.objects.filter(blog=selected_blog).order_by('-created_at')
            messages_qs = Message.objects.filter(post__in=posts).order_by('-created_at')
            for message in messages_qs:
                post_messages[message.post.id].append(message)
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            message_form = MessageForm()

            context = {
                'blogs': blogs,
                'selected_blog': selected_blog,
                'posts': posts,
                'post_messages': post_messages,
                'blog_messages': blog_messages,
                'message_form': message_form,
            }
            return render(request, 'blog/user_blog.html', context)
    return render(request, 'blog/post_message.html', {'blog': blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully.')
        return redirect('user_blogs', user_id=request.user.id)
    return render(request, 'blog/confirm_delete_blog.html', {'blog': blog})
