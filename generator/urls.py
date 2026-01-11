from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('gerar/', views.generate_data, name='generate_data'),
    path('sobre/', views.about, name='about'),
]