from django.shortcuts import get_object_or_404, redirect, render
from quiz.models import *
# Create your views here.

def index(request):
    context = {
        'quizzes': Quiz.objects.all()
    }
    return render(request, 'quiz/index.html', context)


def quiz_details(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        'quiz': quiz,
        'genres': quiz.genres.all(),
        'rounds_count': quiz.rounds.count()
    }
    return render(request, 'quiz/quiz_details.html', context)

def new_game(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    game = Game.objects.create(user=request.user, quiz=quiz)
    return redirect('game', game.id)

def game(request, game_id: int):
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game,
        'quiz': game.quiz,
        'round': game.round
    }
    return render(request, 'quiz/game.html', context)
