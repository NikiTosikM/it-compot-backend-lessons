from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import posts_list
from playlist.views import playlist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/posts_list/', posts_list),
    path('playlist/', playlist)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
