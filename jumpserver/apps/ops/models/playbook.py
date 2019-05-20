from django.db import models


class IisRestart(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE, verbose_name="远程连接用户")
    # task = models.ForeignKey('Tasks', verbose_name="任务", on_delete=models.CASCADE)
    site = models.CharField(max_length=255, verbose_name="任务")
    status = models.IntegerField(verbose_name='执行状态')
    message = models.TextField(verbose_name='返回信息')

    def __str__(self):
        return '%s' % (self.site)

    class Meta:
        verbose_name = 'playbook'
        verbose_name_plural = "playbook"



class File(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE, verbose_name="远程执行用户")
    local_file_path = models.CharField(max_length=255,verbose_name='本地文件路径')
    remove_file_path = models.CharField(max_length=255,verbose_name='远程文件路径')
    status = models.IntegerField(verbose_name='执行状态')
    message = models.TextField(verbose_name='返回信息')



class IisCreate(models.Model):

    hosts = models.ManyToManyField('assets.Asset', verbose_name="主机")
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE, verbose_name="远程连接用户")
    site = models.CharField(max_length=255, verbose_name="站点名")
    dom = models.CharField(max_length=255, verbose_name="绑定域名")
    pool = models.CharField(max_length=255, verbose_name="应用池")
    pdir = models.CharField(max_length=255, verbose_name="物理路径")
    port = models.CharField(max_length=255, verbose_name="监听端口")
    ip = models.CharField(max_length=255, verbose_name="bindip")
    status = models.IntegerField(verbose_name='执行状态')
    pool_message = models.TextField(verbose_name='应用池返回信息')
    site_message = models.TextField(verbose_name='站点返回信息')