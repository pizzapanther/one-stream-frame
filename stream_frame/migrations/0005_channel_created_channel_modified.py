# Generated by Django 4.0.3 on 2022-03-02 19:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stream_frame', '0004_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 3, 2, 19, 44, 31, 122424, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]