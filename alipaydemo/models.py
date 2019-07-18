

from django.db import models


# Create your models here.
from django.utils import timezone


class OrderInfo(models.Model):

    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    money = models.IntegerField(default=0, verbose_name='付款金额')

    class Meta:
        # db_table = 'tb_payment'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.money


class PayInfo(models.Model):
    """
    支付信息
    """
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    trade_id = models.CharField(max_length=100, verbose_name="支付流水号")

    class Meta:
        # db_table = 'tb_payment'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order