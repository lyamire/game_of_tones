import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from quiz.forms import *
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
        'rounds_count': quiz.rounds.count(),
        'can_play': quiz.status == Quiz.Status.APPROVED
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

        answer: str = request.POST.get("answer", "")
        right_answer: Answer = current_question.answers.filter(valid_answer=True).first()
        right_answer_chars = re.sub(r'\W+', '', right_answer.answer.lower()).strip()
        answer_chars = re.sub(r'\W+', '', answer.lower()).strip()
        if right_answer_chars == answer_chars:
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
        game.end_time = datetime.datetime.now(datetime.timezone.utc)
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
        'max_score': questions_count,
        'total_time':game.get_game_time
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
    current_user = request.user
    invites = []
    for game in Game.objects.filter(status=Game.Status.INVITED, user_id=request.user.id).all():
        if game.battle is None:
            continue

        battle: Battle = game.battle
        invite = {
            'game': game,
            'enemy': battle.get_enemy_game(request.user.id).user.username
        }
        invites.append(invite)

    battles_history = []
    for battle in Battle.objects.filter(games__user_id=request.user.id).all():
        enemy_game = battle.get_enemy_game(request.user.id)
        battles_history.append({
            'enemy': enemy_game.user.username,
            'enemy_score': enemy_game.score,
            'my_score': battle.games.filter(user_id=request.user.id).first().score
        })

    context = {
        'invited_games': invites,
        'battles': battles_history,
        'current_user': current_user
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


@login_required()
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


class CreateQuiz(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = 'quiz/create_quiz.html'
    form_class = QuizForm
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        data = super(CreateQuiz, self).get_context_data(**kwargs)
        if self.request.POST:
            data['rounds'] = RoundsFormSet(self.request.POST)
        else:
            data['rounds'] = RoundsFormSet()
        return data

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                form = self.get_form()
                if form.is_valid():
                    quiz = self.object = form.save(commit=False)
                    quiz.status = Quiz.Status.DRAFT
                    quiz.author = request.user
                    quiz.save()
                    form.save_m2m()

                context = self.get_context_data()
                rounds = context['rounds']
                if rounds.is_valid():
                    rounds.save(commit=False)
                    for round_form in rounds:
                        if round_form.is_valid():
                            round = round_form.save(commit=False)
                            round.quiz_id = quiz.id
                            round.save()

                return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            print(e)
            return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('quiz_edit', kwargs={'quiz_id': self.object.id})

@login_required()
def quiz_edit(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not request.user.is_superuser and request.user != quiz.author:
        raise PermissionDenied()

    if quiz.status != Quiz.Status.DRAFT:
        return redirect('quiz_details', quiz_id)

    if request.method == 'GET':
        context = {
            'quiz': quiz,
            'genres': quiz.genres.all(),
            'rounds': quiz.rounds.all()
        }
        return render(request, 'quiz/quiz_edit.html', context)

    if request.method == 'POST':
        quiz.status = Quiz.Status.NEW
        quiz.save()
        return redirect('quiz_details', quiz.id)

@login_required()
def quiz_round_create(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not request.user.is_superuser or request.user != quiz.author:
        raise PermissionDenied()

    if request.method == 'GET':
        context = {
            'quiz': quiz
        }
        return render(request, 'quiz/quiz_round_create.html', context)

    if request.method == 'POST':
        number = request.POST.get("number")
        name = request.POST.get("name")
        description = request.POST.get("description")

        quiz.rounds.create(number=number, name=name, description=description)
        quiz.save()

        return redirect('quiz_edit', quiz_id)

@login_required()
def quiz_round_delete(request, quiz_id: int, round_id: int):
    round = get_object_or_404(Round, quiz_id=quiz_id, id=round_id)
    if not request.user.is_superuser or request.user != round.quiz.author:
        raise PermissionDenied()

    round.delete()
    return redirect('quiz_edit', quiz_id)

@login_required()
def question_create(request, quiz_id: int, round_id: int):
    round = get_object_or_404(Round, quiz_id=quiz_id, id=round_id)
    if not request.user.is_superuser or request.user != round.quiz.author:
        raise PermissionDenied()

    if request.method == 'GET':
        context = {
            "quiz": round.quiz,
            "round": round,
            "attachment_types": Attachment.TypesOfAttachments
        }
        return render(request, 'quiz/question_create.html', context)

    if request.method == 'POST':
        number = request.POST.get("number")
        text = request.POST.get("text")
        attachment_type = request.POST.get("attachment_type")
        file = request.FILES.get("file")
        answers_raw: str = request.POST.get("answers")

        with transaction.atomic():
            question = round.questions.create(text=text, number=number)

            answers = answers_raw.split(r'\r\n')
            for answer in answers:
                text = answer.lstrip('+')
                is_valid = answer.startswith('+') or len(answers) == 1
                question.answers.create(answer=text, valid_answer=is_valid)

            # if question.answers.count(is_valid=True) == 0:
            #     question.answers.first().valid_answer = True

            if file and attachment_type:
                question.attachments.create(attachment_type=attachment_type, file_path=file)

            question.save()

        return redirect('quiz_edit', quiz_id)

@login_required()
def question_delete(request, quiz_id: int, round_id: int, question_id: int):
    question = get_object_or_404(Question, round__quiz_id=quiz_id, round_id=round_id, id=question_id)
    if not request.user.is_superuser or request.user != question.round.quiz.author:
        raise PermissionDenied()

    question.delete()
    return redirect('quiz_edit', quiz_id)
