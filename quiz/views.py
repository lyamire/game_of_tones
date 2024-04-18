from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from quiz.models import *

def index(request):
    context = {
        'quizzes': Quiz.objects.filter(status=Quiz.Status.APPROVED).all()
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

@login_required
def new_game(request, quiz_id: int):
    game = create_game_for_user(request.user.id, quiz_id)
    return redirect('round_details', game.id, game.quiz.rounds.first().id)

@login_required
def play_game(request, game_id: int):
    game = get_object_or_404(Game, pk=game_id, user=request.user)
    return redirect('round_details', game.id, game.quiz.rounds.first().id)

def create_game_for_user(user_id, quiz_id) -> Game:
    return Game.objects.create(user_id=user_id, quiz_id=quiz_id)

@login_required
def round_details(request, game_id: int, round_id: int):
    game = get_object_or_404(Game, id=game_id)
    round_info: Round = game.quiz.rounds.filter(id=round_id).first()
    first_question: Question = round_info.questions.order_by('number').first()
    context = {
        'game': game,
        'quiz': game.quiz,
        'round': round_info,
        'first_question_id': first_question.id,
    }
    return render(request, 'quiz/round_details.html', context)

@login_required
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
        game.status = Game.Status.ACTIVE

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

        game.status = Game.Status.FINISHED
        game.save()

        return redirect('result_details', game.id)

def download_file(request, file_id):
    uploaded_file = Attachment.objects.get(pk=file_id)
    return FileResponse(uploaded_file.file_path.file)

def download_icon(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    return FileResponse(genre.icon.file)

@login_required
def result_details(request, game_id: int):
    game = get_object_or_404(Game, id=game_id)

    questions_count = 0
    for round in game.quiz.rounds.all():
        questions_count += round.questions.count()

    context = {
        'game': game,
        'quiz': game.quiz,
        'score': game.score,
        'max_score': questions_count
    }
    return render(request, 'quiz/result_details.html', context)


def genres(request):
    context = {
        'genres': Genre.objects.all()
    }
    Genre.objects.prefetch_related(Quiz.__name__)
    return render(request, 'quiz/genres.html', context)


def rating(request, quiz_id: int):
    quiz = Quiz.objects.get(id=quiz_id)
    games = quiz.games.order_by('-score').all()

    scores = {}
    for game in games:
        if game.user.id not in scores:
            scores[game.user.id] = game

    context = {
        'games': scores.values(),
        'quiz': quiz,
    }

    return render(request, 'quiz/rating.html', context)


def rules(request):
    return render(request, 'quiz/rules.html')

@login_required
def battles(request):
    invites = []
    for game in Game.objects.filter(status=Game.Status.INVITED, user_id=request.user.id).all():
        if game.battle is None:
            continue

        battle: Battle = game.battle
        enemy: User = [game.user for game in battle.games.all() if game.user.id != request.user.id][0]
        invite = {
            'game': game,
            'enemy': enemy.username
        }
        invites.append(invite)

    context = {
        'invited_games': invites
    }

    return render(request, 'quiz/battles.html', context)


@login_required
def new_battle(request):
    if request.method == 'GET':
        context = {
            'users': User.objects.exclude(id=request.user.id).all(),
        }
        return render(request, 'quiz/new_battle.html', context)
    if request.method == 'POST':
        invited_user_id = request.POST.get("user_id")

        quiz = generate_quiz_for_battle()

        battle = Battle.objects.create(quiz_id=quiz.id)

        our_game = create_game_for_user(request.user.id, quiz.id)
        battle.games.add(our_game)

        invited_game = create_game_for_user(invited_user_id, quiz.id)
        invited_game.status = Game.Status.INVITED
        invited_game.save()
        battle.games.add(invited_game)

        battle.save()

        return redirect('round_details', our_game.id, our_game.quiz.rounds.first().id)


def generate_quiz_for_battle():
    quiz = Quiz.objects.create(status=Quiz.Status.ONE_TIME)
    round = quiz.rounds.create(name="Батл", description="Случайная выборка вопросов")

    all_questions = Question.objects.filter(round__quiz__status=Quiz.Status.APPROVED).order_by('?')[:10]

    for source_question in all_questions:
        question = round.questions.create(number=round.questions.count(),
                                          text=source_question.text)

        for source_answer in source_question.answers.all():
            question.answers.create(answer=source_answer.answer, valid_answer=source_answer.valid_answer)

        attach: Attachment = source_question.attachments.first()
        question.attachments.create(attachment_type=attach.attachment_type,
                                    file_path=attach.file_path)

    quiz.save()
    return quiz

