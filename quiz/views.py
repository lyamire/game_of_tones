from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

import quiz
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
    round_info: Round = game.quiz.rounds.filter(id=round_id).first()
    first_question: Question = round_info.questions.order_by('number').first()
    context = {
        'game': game,
        'round': round_info,
        'first_question_id': first_question.id,
    }
    return render(request, 'quiz/round_details.html', context)

def question_details(request, game_id: int, round_id: int, question_id: int):
    game = get_object_or_404(Game, id=game_id)
    round_info: Round = game.quiz.rounds.filter(id=round_id).first()
    current_question: Question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        context = {
            'game': game,
            'quiz': game.quiz,
            'round': round_info,
            'question': current_question,
            'answers': current_question.answers.all(),
            'file': current_question.attachments.first()
        }
        return render(request, 'quiz/question_details.html', context)
    if request.method == 'POST':
        answer = request.POST.get("answer", "")
        right_answer: Answer = current_question.answers.filter(valid_answer=True).first()
        if right_answer.answer == answer:
            game.score += 1
            game.save()

        next_question: Question = round_info.get_question_after(question_num=current_question.number)
        if next_question:
            game.question_number = next_question.number
            game.save()
            return redirect('question', game.id, round_id, next_question.id)
        else:
            next_round: Round = game.quiz.get_round_after(round_info.number)
            if next_round:
                return redirect('round_details', game.id, next_round.id)

        # TODO
        return redirect('result', game.id)

def download_file(request, file_id):
    uploaded_file = Attachment.objects.get(pk=file_id)
    return FileResponse(uploaded_file.file_path.file)