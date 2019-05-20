# Generated by Django 2.1.7 on 2019-04-15 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0026_auto_20190415_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crontabtask',
            name='crontab_day',
            field=models.CharField(max_length=32, verbose_name='定时任务-天'),
        ),
        migrations.AlterField(
            model_name='crontabtask',
            name='crontab_hour',
            field=models.CharField(max_length=32, verbose_name='定时任务-时'),
        ),
        migrations.AlterField(
            model_name='crontabtask',
            name='crontab_minute',
            field=models.CharField(max_length=32, verbose_name='定时任务—分'),
        ),
        migrations.AlterField(
            model_name='crontabtask',
            name='crontab_month',
            field=models.CharField(max_length=32, verbose_name='定时任务-月'),
        ),
        migrations.AlterField(
            model_name='crontabtask',
            name='crontab_week',
            field=models.CharField(max_length=32, verbose_name='定时任务-周'),
        ),
    ]
