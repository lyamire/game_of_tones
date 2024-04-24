from django.contrib import admin
from .models import Genre, Quiz, Round, Question, Attachment, Answer

# Register your models here.

admin.site.register(Genre)
# admin.site.register(Rounds)
# admin.site.register(Attachments)
# admin.site.register(Answers)

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
    list_filter = ['status']
    list_display = ["name", 'level', 'status', 'author']
    inlines = [RoundInline]

class QuestionInline(admin.TabularInline):
    model = Question
    verbose_name = "Questions"
    extra = 1

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
