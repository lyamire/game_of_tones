from django.contrib import admin
from .models import Profile, Genres, Quizzes, Rounds, Questions, Attachments, Answers, Results, Battles
# Register your models here.

admin.site.register(Profile)
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

class AnswersInline(admin.TabularInline):
    model = Answers
    verbose_name = "Answers"
    extra = 1
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["title", 'quiz', 'round']
    list_filter = ['quiz', 'round']
    inlines = [AttachmentInline, AnswersInline]

class RoundsInline(admin.TabularInline):
    model = Rounds
    verbose_name = "Rounds"
    extra = 1

@admin.register(Quizzes)
class QuizzesAdmin(admin.ModelAdmin):
    list_display = ["quiz_name", 'level']
    inlines = [RoundsInline]
