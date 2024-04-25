import datetime
from typing import List

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50)
    icon = models.FileField(upload_to='./files/covers', null=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    class Status(models.TextChoices):
        DRAFT = "Draft", _('Draft')
        NEW = "New", _('New')
        APPROVED = "Approved", _('Approved')
        REJECTED = "Rejected", _('Rejected')
        ONE_TIME = "One_Time", _('One_Time')

    class Level(models.TextChoices):
        EASY = "Easy", _('Easy')
        HARD = "Hard", _('Hard')

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    genres = models.ManyToManyField(Genre, related_name='quizzes', verbose_name='Жанры')
    level = models.CharField(max_length=4, choices=Level.choices, default=Level.EASY)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    author = models.ForeignKey(User, related_name='quizzes', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_round_after(self, round_num):
        return self.rounds.order_by('number').filter(number__gt=round_num).first()


class Round(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='rounds', on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.quiz.name} - {self.name}'

    def get_question_after(self, question_num):
        return self.questions.order_by('number').filter(number__gt=question_num).first()


class Question(models.Model):
    round = models.ForeignKey(Round, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    number = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.round}'

    @admin.display(
        description='Answer the question'
    )
    def get_valid_answer(self):
        answers: List[Answer] = self.answers.filter(valid_answer=True)
        if len(answers) == 0:
            return 'No answer'
        return f'{answers[0].answer}'


class Attachment(models.Model):
    class TypesOfAttachments(models.TextChoices):
        IMG = "IMG", _('Image')
        AUD = "AUD", _('Audio')
        VID = "VID", _('Video')

    question = models.ForeignKey(Question, related_name='attachments', on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=20, choices=TypesOfAttachments)
    file_path = models.FileField(upload_to='./attachments')

    def __str__(self):
        return self.file_path.name


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField(max_length=50)
    valid_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question} - {self.answer} - {self.valid_answer}'


class Battle(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='battle', on_delete=models.CASCADE)

    def get_enemy_game(self, current_user_id):
        enemy_game: Game = self.games.exclude(user_id=current_user_id).first()
        return enemy_game


class Game(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _('Active')
        FINISHED = "FINISHED", _('Finished')
        INVITED = "INVITED", _('Invited')

    user = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='games', on_delete=models.CASCADE)
    round_num = models.ForeignKey(Round, related_name='rounds', on_delete=models.CASCADE, default=1)
    question_number = models.PositiveSmallIntegerField(default=0)
    start_time = models.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    score = models.PositiveSmallIntegerField(default=0)
    battle = models.ForeignKey(Battle, related_name='games', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.quiz.name} - {self.score}'

    @property
    def get_game_time(self):
        if not self.end_time or not self.start_time:
            return 'Not finished'
        td = self.end_time - self.start_time
        td -= datetime.timedelta(microseconds=td.microseconds)
        return str(td)
