from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rules/', views.rules, name='rules'),
    path('genres/', views.genres, name='genres'),
    path('genres/<int:genre_id>/icon', views.download_icon, name='icon'),
    path('quiz/new', views.CreateQuiz.as_view(), name="create_quiz"),
    path('quiz/<int:quiz_id>/', views.quiz_details, name='quiz_details'),
    path('quiz/<int:quiz_id>/edit', views.quiz_edit, name='quiz_edit'),
    path('quiz/<int:quiz_id>/round', views.quiz_round_create, name='quiz_round_create'),
    path('quiz/<int:quiz_id>/round/<int:round_id>/delete', views.quiz_round_delete, name='quiz_round_delete'),
    path('quiz/<int:quiz_id>/round/<int:round_id>/question', views.question_create, name='question_create'),
    path('quiz/<int:quiz_id>/round/<int:round_id>/question/<int:question_id>/delete', views.question_delete,
         name='question_delete'),
    path('quiz/<int:quiz_id>/play', views.new_game, name='new_game'),
    path('quiz/<int:quiz_id>/rating/', views.rating, name='rating'),
    path('game/<int:game_id>/', views.play_game, name='play_game'),
    path('game/<int:game_id>/round/<int:round_id>/', views.round_details, name='round_details'),
    path('game/<int:game_id>/round/<int:round_id>/question/<int:question_id>/', views.question_details,
         name='question'),
    path('game/<int:game_id>/result/', views.result_details, name='result_details'),
    path('file/<int:file_id>/', views.download_file, name='file'),
    path('battles/', views.battles, name='battles'),
    path('battles/new', views.new_battle, name='new_battle'),
]