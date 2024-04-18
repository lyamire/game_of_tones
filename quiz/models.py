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
        NEW = "New", _('New')
        APPROVED = "Approved", _('Approved')
        REJECTED = "Rejected", _('Rejected')
        ONE_TIME = "One_Time", _('One_Time')

    class Level(models.TextChoices):
        EASY = "Easy", _('Easy')
        HARD = "Hard", _('Hard')

    name = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='quizzes')
    level = models.CharField(max_length=4, choices=Level.choices, default=Level.EASY)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return self.name

    def get_round_after(self, round_num):
        return self.rounds.order_by('number').filter(number__gt=round_num).first()


class Round(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='rounds', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    number = models.IntegerField(default=0)

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
        if answers is None:
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
