# Generated by Django 2.2.4 on 2019-08-07 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='user',
        ),
    ]