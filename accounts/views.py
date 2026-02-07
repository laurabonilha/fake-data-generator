from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.username}!')
            return redirect('generator:home')
        else:
            messages.error(request, 'Erro ao criar conta. Por favor, verifique os dados.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
