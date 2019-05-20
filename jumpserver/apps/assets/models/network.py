from django.db import models
from django.utils.translation import ugettext_lazy as _

def default_node():
    try:
        from .node import Node
        root = Node.root()
        return root
    except:
        return None

class NetworkDevice(models.Model):
    """网络设备"""

    net_name = models.CharField(max_length=128,verbose_name="设备名称")
    sub_asset_type = models.CharField(max_length=128, verbose_name="网络设备类型")

    ip1 = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP1")
    ip2 = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP2")

    model = models.CharField(max_length=128, null=True, blank=True, verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="详细配置")
    #node = models.ManyToManyField("NetworkDeviceNode",blank=True,null=True)
    node = models.ManyToManyField('assets.Node', default=default_node,  verbose_name=_("Nodes"))
    m_time = models.DateTimeField(auto_now=True, verbose_name='改动日期')
    message = models.TextField(null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return '%s--%s--%s' % (self.net_name, self.sub_asset_type, self.model)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"



class IdcNode(models.Model):
    node_name = models.OneToOneField('assets.Node', unique=True, on_delete=models.CASCADE)
    m_time = models.DateTimeField(auto_now=True, verbose_name='改动日期')
    addr = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"地址")
    user = models.CharField(max_length=30, null=True, blank=True, verbose_name=u"联系人")
    tel = models.CharField(max_length=30, null=True, blank=True, verbose_name=u"联系人电话")
    message = models.TextField(null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return '%s--%s' % (self.node_name, self.m_time)

    class Meta:
        verbose_name = '网络设备节点'
        verbose_name_plural = "网络设备节点"