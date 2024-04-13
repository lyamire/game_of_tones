from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_details(request):
    profile: Profile = Profile.objects.get_or_create(user=request.user)[0]

    games = {}
    for game in profile.user.games.order_by('-score').all():
        if game.quiz.id in games:
            continue
        games[game.quiz.id] = game

    if request.method == 'GET':
        context = {
            'profile': profile,
            'games': games.values()
        }

        return render(request, 'accounts/profile.html', context)
    if request.method == 'POST':
        first_name: str = request.POST.get('first_name')
        last_name: str = request.POST.get('last_name')
        email: str = request.POST.get('email')

        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.email = email
        profile.user.save()

        return redirect('accounts:profile')
