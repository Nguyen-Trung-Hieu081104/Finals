from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Homepage showing list of posts
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Detail page for a single post
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('message_board/', views.message_board, name='message_board'),
    path('post_message/', views.post_message, name='post_message'),
    path('profile/', views.profile, name='profile'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('user_blogs/<int:user_id>/', views.user_blogs, name='user_blogs'),
    path('post/<int:post_id>/post_message/', views.post_message_on_post, name='post_message_on_post'),
    path('blog/<int:blog_id>/post_message/', views.post_message_on_blog, name='post_message_on_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
]
