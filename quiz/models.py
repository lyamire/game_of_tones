from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user)

class Genres(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre


class Quizzes(models.Model):
    class Level(models.TextChoices):
        EASY = "Easy", _('Easy')
        HARD = "Hard", _('Hard')

    quiz_name = models.CharField(max_length=100)
    quiz_description = models.TextField()
    genre = models.ForeignKey(Genres, related_name='genres', on_delete=models.CASCADE)
    level = models.CharField(max_length=4, choices=Level.choices, default=Level.EASY)

    def __str__(self):
        return self.quiz_name

class Rounds(models.Model):
    round_name = models.CharField(max_length=50)
    round_description = models.TextField()

    def __str__(self):
        return self.round_name

class Questions(models.Model):
    quiz = models.ForeignKey(Quizzes, related_name='quizzes', on_delete=models.CASCADE)
    round = models.ForeignKey(Rounds, related_name='rounds', on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Attachments(models.Model):
    class TypesOfAttachments(models.TextChoices):
        IMG = "IMG", _('Image')
        AUD = "AUD", _('Audio')
        VID = "VID", _('Video')

    question = models.ForeignKey(Questions, related_name='attachments', on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=20, choices=TypesOfAttachments)
    file_path = models.FileField(upload_to='./attachments')

    def __str__(self):
        return self.file_path.name

class Answers(models.Model):
    question = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField(max_length=50)
    valid_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class Results(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)

    def __str__(self):
        return f'{str(self.user.nickname)} - {self.quiz} - {self.result}'

class Battles(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    first_user = models.ForeignKey(Profile, related_name='first_user', on_delete=models.CASCADE)
    second_user = models.ForeignKey(Profile, related_name='second_user', on_delete=models.CASCADE)

    def __str__(self):
        return f'Battle between {self.first_user} and {self.second_user} in {self.quiz.quiz_name} '
