# Generated by Django 5.0.4 on 2024-04-11 11:47

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_rename_round_game_round_num_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='round',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 11, 11, 47, 53, 981865, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.round'),
        ),
    ]
