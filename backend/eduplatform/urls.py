from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/',      include('users.urls')),
    path('api/v1/courses/',   include('courses.urls')),
    path('api/v1/attendance/',include('attendance.urls')),
    path('api/v1/tests/',     include('exams.urls')),
    path('api/v1/fees/',      include('fees.urls')),
    path('api/v1/notices/',   include('notices.urls')),
    path('api/v1/',           include('api.urls')),

    # API Docs
    path('api/schema/',    SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
