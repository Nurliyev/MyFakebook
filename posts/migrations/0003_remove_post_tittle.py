# Generated by Django 3.2.3 on 2021-06-08 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tittle',
        ),
    ]
