# Generated by Django 5.0.4 on 2024-04-18 21:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_remove_battle_games_game_battle_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='round',
            old_name='quizzes',
            new_name='quiz',
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 18, 21, 2, 13, 634118, tzinfo=datetime.timezone.utc)),
        ),
    ]
