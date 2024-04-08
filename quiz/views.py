from django.shortcuts import get_object_or_404, render
from quiz.models import *
# Create your views here.

def index(request):
    context = {
        'quizzes': Quizzes.objects.all()
    }
    return render(request, 'quiz/index.html', context)


def quiz_details(request, quiz_id: int):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    context = {
        'quiz': quiz,
        'genres': quiz.genres.all(),
    }
    return render(request, 'quiz/quiz_details.html', context)
