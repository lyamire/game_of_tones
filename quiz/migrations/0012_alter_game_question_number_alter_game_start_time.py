# Generated by Django 5.0.4 on 2024-04-09 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_game_question_number_alter_game_round_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='question_number',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 9, 20, 20, 16, 189092, tzinfo=datetime.timezone.utc)),
        ),
    ]
