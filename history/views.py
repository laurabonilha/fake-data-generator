from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GenerationHistory

@login_required
def my_history(request):
    """View para listar o histórico de gerações do usuário logado."""
    history_list = GenerationHistory.objects.filter(user=request.user)
    
    return render(request, 'history/my_history.html', {
        'history_list': history_list
    })
