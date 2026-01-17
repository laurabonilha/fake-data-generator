# generator/api/urls.py
"""URLs da API REST."""
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import GeneratePersonAPIView, GenerateCompanyAPIView, APIRootView

app_name = 'api'

urlpatterns = [
    # Root da API
    path('', APIRootView.as_view(), name='api-root'),
    
    # Endpoints de geração
    path('generate/person/', GeneratePersonAPIView.as_view(), name='generate-person'),
    path('generate/company/', GenerateCompanyAPIView.as_view(), name='generate-company'),
    
    # Documentação da API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]