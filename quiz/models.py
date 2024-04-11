import datetime
from typing import List

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user)

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    class Level(models.TextChoices):
        EASY = "Easy", _('Easy')
        HARD = "Hard", _('Hard')

    name = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='genres')
    level = models.CharField(max_length=4, choices=Level.choices, default=Level.EASY)

    def __str__(self):
        return self.name

    def get_round_after(self, round_id):
        return self.rounds.order_by('id').filter(id__gt=round_id).first()


class Round(models.Model):
    quizzes = models.ForeignKey(Quiz, related_name='rounds', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    # number = models.

    def __str__(self):
        return f'{self.quizzes.name} - {self.name}'

    def get_question_after(self, question_id):
        return self.questions.order_by('id').filter(id__gt=question_id).first()


class Question(models.Model):
    round = models.ForeignKey(Round, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

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

class Game(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _('Active')
        FINISHED = "FINISHED", _('Finished')

    user = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='games', on_delete=models.CASCADE)
    round_num = models.ForeignKey(Round, related_name='rounds', on_delete=models.CASCADE, default=1)
    question_number = models.PositiveSmallIntegerField(default=0)
    start_time = models.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.quiz.name} - {self.score}'
class Result(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)

    def __str__(self):
        return f'{str(self.user.nickname)} - {self.quiz} - {self.result}'

class Battle(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    first_user = models.ForeignKey(Profile, related_name='first_user', on_delete=models.CASCADE)
    second_user = models.ForeignKey(Profile, related_name='second_user', on_delete=models.CASCADE)

    def __str__(self):
        return f'Battle between {self.first_user} and {self.second_user} in {self.quiz.name} '
