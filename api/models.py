from django.db import models


# Create your models here.
# from goods.models import GoodsInfo, CartItem
# from user.models import UserInfo


class Payment1(models.Model):
    name = models.CharField(max_length=30)
    order_id = models.CharField(max_length=70)
    trade_id = models.CharField(max_length=70)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    app_id = models.CharField(max_length=30)
    seller_id = models.CharField(max_length=20)
    timestamp = models.CharField(max_length=20)

    def __str__(self):
        return self.order_id  # 和Java中的toString方法相同

    class Meta:
        db_table = 'api_payment1'
        verbose_name = '订单记录'
        verbose_name_plural = verbose_name
