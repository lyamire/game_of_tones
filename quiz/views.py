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
    return redirect('round_details', game.id, quiz.rounds.first().id)

def round_details(request, game_id: int, round_id: int):
    game = get_object_or_404(Game, id=game_id)
    round_info = game.quiz.rounds.filter(id=round_id).first()
    context = {
        'game': game,
        'round': round_info
    }
    return render(request, 'quiz/round_details.html', context)

def question_details(request, game_id: int, round_id: int, question_id: int):
    if request.method == 'GET':
        game = get_object_or_404(Game, id=game_id)
        round_info: Round = game.quiz.rounds.filter(id=round_id).first()
        current_question: Question = get_object_or_404(Question, id=question_id)
        # round_info.round_q
        # round_info.quizzes
        context = {
            'game': game,
            'quiz': game.quiz,
            'round': round_info,
            'question': current_question,
            'answers': current_question.answers.all()
        }
        return render(request, 'quiz/question_detail.html', context)
    if request.method == 'POST':
        pass