from django.contrib import admin
from .models import Profiles, Genres, Quizzes, Rounds, Questions, Attachments, Answers, Results, Battles
# Register your models here.

admin.site.register(Profiles)
admin.site.register(Genres)
# admin.site.register(Rounds)
# admin.site.register(Attachments)
# admin.site.register(Answers)
# admin.site.register(Results)
# admin.site.register(Battles)

class AttachmentInline(admin.TabularInline):
    model = Attachments
    verbose_name = "Attachment"
    extra = 0

class AnswerInline(admin.TabularInline):
    model = Answers
    verbose_name = "Answers"
    extra = 1

@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['round']
    list_display = ["get_valid_answer", 'round']
    inlines = [AttachmentInline, AnswerInline]

class RoundInline(admin.TabularInline):
    model = Rounds
    verbose_name = "Rounds"
    extra = 1

@admin.register(Quizzes)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["name", 'level']
    inlines = [RoundInline]
