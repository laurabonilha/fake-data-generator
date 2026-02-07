from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('generator.urls')),
    path('accounts/', include('accounts.urls')),
    path('history/', include('history.urls')),
    path('api/v1/', include('generator.api.urls')),
]
