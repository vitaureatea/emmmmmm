# Generated by Django 2.1.7 on 2019-03-14 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0029_auto_20190314_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkdevice',
            name='sub_asset_type',
            field=models.CharField(max_length=128, verbose_name='网络设备类型'),
        ),
    ]