# Generated by Django 2.1.7 on 2019-04-17 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0030_auto_20190417_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crontabtask',
            name='hosts',
        ),
        migrations.RemoveField(
            model_name='crontabtask',
            name='run_as',
        ),
    ]
