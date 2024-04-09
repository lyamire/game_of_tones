from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>', views.quiz_details, name='quiz_details'),
    path('game/<int:quiz_id>', views.new_game, name='new_game'),
    path('game/<int:game_id>/play', views.game, name='game'),
]