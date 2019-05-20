# Generated by Django 2.1.7 on 2019-03-14 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0025_auto_20190221_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net_name', models.CharField(max_length=128, verbose_name='设备名称')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')], default=0, verbose_name='网络设备类型')),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='网络设备型号')),
                ('firmware', models.CharField(blank=True, max_length=128, null=True, verbose_name='设备固件版本')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='详细配置')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='改动日期')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NetworkDeviceNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_name', models.CharField(max_length=64, unique=True)),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='改动日期')),
            ],
            options={
                'verbose_name': '网络设备节点',
                'verbose_name_plural': '网络设备节点',
            },
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='node',
            field=models.ManyToManyField(blank=True, null=True, to='assets.NetworkDeviceNode'),
        ),
    ]