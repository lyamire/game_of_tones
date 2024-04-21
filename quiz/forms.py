from django import forms
from django.forms import inlineformset_factory

from quiz.models import Quiz, Round, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'genres']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название квиза', 'autofocus': 'autofocus'},),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': 'Описание квиза'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название раунда'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': 'Описание раунда'}),
        }


RoundsFormSet = inlineformset_factory(
    Quiz, Round, form=RoundForm,
    fields=['id', 'name', 'description'],
    extra=1, can_delete=False, can_delete_extra=True,
)
