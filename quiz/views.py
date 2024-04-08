from django.shortcuts import get_object_or_404, render
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
