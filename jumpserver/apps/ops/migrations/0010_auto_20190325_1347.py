# Generated by Django 2.1.7 on 2019-03-25 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0009_file_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task_module',
            field=models.CharField(max_length=64, verbose_name='模块'),
        ),
    ]