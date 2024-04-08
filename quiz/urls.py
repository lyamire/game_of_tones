from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>', views.quiz_details, name='quiz_details'),
]