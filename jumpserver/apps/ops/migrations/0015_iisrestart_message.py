# Generated by Django 2.1.7 on 2019-03-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0014_remove_iisrestart_messag'),
    ]

    operations = [
        migrations.AddField(
            model_name='iisrestart',
            name='message',
            field=models.CharField(default=1, max_length=255, verbose_name='返回信息'),
            preserve_default=False,
        ),
    ]
