# Generated by Django 2.1.7 on 2019-03-14 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0026_auto_20190314_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkdevice',
            name='node',
            field=models.ManyToManyField(to='assets.NetworkDeviceNode'),
        ),
    ]