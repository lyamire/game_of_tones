from django.contrib import admin
from .models import Profile, Genre, Quiz, Round, Question, Attachment, Answer, Result, Battle
# Register your models here.

admin.site.register(Profile)
admin.site.register(Genre)
# admin.site.register(Rounds)
# admin.site.register(Attachments)
# admin.site.register(Answers)
# admin.site.register(Results)
# admin.site.register(Battles)

class AttachmentInline(admin.TabularInline):
    model = Attachment
    verbose_name = "Attachment"
    extra = 0

class AnswerInline(admin.TabularInline):
    model = Answer
    verbose_name = "Answers"
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['round']
    list_display = ["get_valid_answer", 'round']
    inlines = [AttachmentInline, AnswerInline]

class RoundInline(admin.TabularInline):
    model = Round
    verbose_name = "Rounds"
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["name", 'level']
    inlines = [RoundInline]
