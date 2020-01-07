from django.db import models

from user.models import *


# Create your models here.

class TypeInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='种类')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goods_typeinfo'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20, verbose_name='商品名')
    gpic = models.ImageField(upload_to='goods', verbose_name='图片')
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='价格')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    gunit = models.CharField(max_length=20, default="500克", verbose_name='单位')
    gclick = models.IntegerField(verbose_name='点击量')
    gjianjie = models.CharField(max_length=50, verbose_name='简介')
    gcontext = models.CharField(max_length=100, verbose_name='详细介绍')
    gkucun = models.IntegerField(verbose_name='库存')
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name='种类')  # one(type) to many(good)

    def __str__(self):
        return self.gtitle

    class Meta:
        db_table = 'goods_goodsinfo'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class CartItem(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='所属用户')
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name='商品')
    num = models.IntegerField(verbose_name='数量')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品小计", default=0)