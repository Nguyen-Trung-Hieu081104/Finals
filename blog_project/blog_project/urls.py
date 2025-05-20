from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('blog.urls')),
    path('', include('blog.urls')),
    path('', blog_views.home, name='home'),  # homepage

    path('signup/', blog_views.signup, name='signup'),
    path('message_board/', blog_views.message_board, name='message_board'),
    path('post_message/', blog_views.post_message, name='post_message'),
    path('delete/<int:message_id>/', blog_views.delete_message, name='delete_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
