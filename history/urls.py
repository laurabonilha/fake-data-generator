from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('meus-registros/', views.my_history, name='my_history'),
]
