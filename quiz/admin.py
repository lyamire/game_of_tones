from django.contrib import admin
from .models import Profile, Genres, Quizzes, Rounds, Questions, Attachments, Answers, Results, Battles
# Register your models here.

admin.site.register(Profile)
admin.site.register(Genres)
admin.site.register(Quizzes)
admin.site.register(Rounds)
admin.site.register(Questions)
admin.site.register(Attachments)
admin.site.register(Answers)
admin.site.register(Results)
admin.site.register(Battles)


