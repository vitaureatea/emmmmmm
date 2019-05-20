from django.db import models


class BusinessNode(models.Model):
    name = models.OneToOneField('assets.Node', unique=True, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return '%s' % (self.net_name,)

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"