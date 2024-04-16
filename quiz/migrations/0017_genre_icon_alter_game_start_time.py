# Generated by Django 5.0.4 on 2024-04-16 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_alter_game_start_time_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='icon',
            field=models.FileField(null=True, upload_to='./files/covers'),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 13, 47, 11, 457079, tzinfo=datetime.timezone.utc)),
        ),
    ]
