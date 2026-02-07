"""
URL configuration for Drag'n'Scroll project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls')),
    path('api/user/', include('core.urls')),
    path('api/learning/', include('learning.urls')),
    path('api/vocab/', include('vocab.urls')),
    path('api/course/', include('course.urls')),
    path('api/video/', include('video_app.urls')),
    path('api/chat/', include('chat.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
