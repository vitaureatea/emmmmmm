from django.db import models


class CrontabTask(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE, verbose_name="远程连接用户")
    name = models.CharField(max_length=128, verbose_name='定时任务名称')
    crontab_minute = models.CharField(max_length=32, verbose_name='定时任务—分')
    crontab_hour = models.CharField(max_length=32, verbose_name='定时任务-时')
    crontab_day = models.CharField(max_length=32, verbose_name='定时任务-天')
    crontab_month = models.CharField(max_length=32, verbose_name='定时任务-月')
    crontab_week = models.CharField(max_length=32, verbose_name='定时任务-周')
    scripts_path = models.CharField(max_length=128, verbose_name='脚本路径')
    crontab_log = models.TextField(verbose_name='返回结果')
    status = models.IntegerField(verbose_name='执行状态')
    comment = models.TextField(verbose_name='备注信息')


class GetCrontab(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    message = models.TextField(verbose_name='返回结果')


class GetIISSite(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    message = models.TextField(verbose_name='返回结果')