from django import template
from quiz.models import *

register = template.Library()


@register.inclusion_tag('quiz/battle_invites_count.html')
def get_battle_invites_count(user_id: int):
    return {
        'count': Battle.objects.filter(games__user_id=user_id, games__status=Game.Status.INVITED).count()
    }
