from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>/', views.quiz_details, name='quiz_details'),
    path('game/<int:quiz_id>/', views.new_game, name='new_game'),
    path('game/<int:game_id>/round/<int:round_id>/', views.round_details, name='round_details'),
    path('game/<int:game_id>/round/<int:round_id>/question/<int:question_id>/', views.question_details,
         name='question'),
    path('game/<int:game_id>/result/', views.result_details, name='result_details'),
    path('file/<int:file_id>/', views.download_file, name='file'),
    path('genres/', views.genres, name='genres'),
    path('quiz/<int:quiz_id>/rating/', views.rating, name='rating'),
]