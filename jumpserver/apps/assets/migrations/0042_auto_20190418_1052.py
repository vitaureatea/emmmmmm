# Generated by Django 2.1.7 on 2019-04-18 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0041_auto_20190409_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='platform',
            field=models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('Windows2016', 'Windows(2016)')], default='Linux', max_length=128, verbose_name='Platform'),
        ),
    ]
