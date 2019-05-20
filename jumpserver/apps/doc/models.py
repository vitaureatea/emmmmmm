from django.db import models


class Doc(models.Model):
    update_user = models.CharField(max_length=32, verbose_name='上次更新用户')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    doc_value = models.TextField(verbose_name='内容')


class OpsDoc(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)
    cuser = models.CharField(max_length=32, null=False)
    uuser = models.CharField(max_length=32, null=False)
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)