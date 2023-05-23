from django.shortcuts import render, redirect
from connexion.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f'Coucou {username}, Votre compte à été créé avec succès !')
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'connexion/register.html', {'form': form})
