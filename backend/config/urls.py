"""
URL configuration for Drag'n'Scroll project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.conf.urls import url
from core.views import health_check
import os
import mimetypes
from pathlib import Path

def serve_media_file(request, file_path):
    """
    Serve media files in production (when DEBUG=False)
    This allows uploaded videos to be accessed
    """
    media_root = Path(settings.MEDIA_ROOT)
    file_path = file_path.lstrip('/')  # Remove leading slash
    full_path = media_root / file_path

    # Security check - ensure the path is within MEDIA_ROOT
    if not str(full_path.resolve()).startswith(str(media_root.resolve())):
        return HttpResponse('Unauthorized', status=401)

    if not full_path.exists():
        return HttpResponse('File not found', status=404)

    # Determine content type
    content_type, _ = mimetypes.guess_type(str(full_path))
    if content_type is None:
        content_type = 'application/octet-stream'

    # Serve the file
    with open(full_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(full_path)}"'
        return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls')),
    path('api/user/', include('core.urls')),
    path('api/learning/', include('learning.urls')),
    path('api/vocab/', include('vocab.urls')),
    path('api/course/', include('course.urls')),
    path('api/video/', include('video.urls')),
    path('api/chat/', include('chat.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve media files in production
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve_media_file, name='serve_media'),
    ]
