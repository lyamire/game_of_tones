# Generated by Django 5.0.4 on 2024-04-18 14:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_remove_battle_games_alter_battle_quiz_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='games',
        ),
        migrations.AddField(
            model_name='game',
            name='battle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='quiz.battle'),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 18, 14, 32, 12, 872281, tzinfo=datetime.timezone.utc)),
        ),
    ]
