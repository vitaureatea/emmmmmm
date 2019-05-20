# Generated by Django 2.1.7 on 2019-04-18 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0042_auto_20190418_1052'),
        ('ops', '0031_auto_20190417_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetCrontab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='返回结果')),
                ('hosts', models.ManyToManyField(to='assets.Asset', verbose_name='主机')),
                ('run_as', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.SystemUser', verbose_name='远程连接用户')),
            ],
        ),
        migrations.RemoveField(
            model_name='crontablog',
            name='corntab_task',
        ),
        migrations.AddField(
            model_name='crontabtask',
            name='crontab_log',
            field=models.TextField(default='1', verbose_name='返回结果'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crontabtask',
            name='hosts',
            field=models.ManyToManyField(to='assets.Asset', verbose_name='主机'),
        ),
        migrations.AddField(
            model_name='crontabtask',
            name='run_as',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='assets.SystemUser', verbose_name='远程连接用户'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CrontabLog',
        ),
    ]
