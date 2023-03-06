from django.db import models

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(
        verbose_name='部门',
        max_length=16)
    def __str__(self):
        return self.position

class Personnel(models.Model):
    pid = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=16)
    pwd = models.CharField(max_length=16)
    pos = models.ForeignKey(verbose_name='职位',
        to='Position', to_field='id', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

class OrderTable(models.Model):
    '''header'''
    oid = models.IntegerField(verbose_name='订单编号', unique=True)
    date = models.DateField(verbose_name='日期')
    customer = models.ForeignKey(verbose_name='订货人', to='Customer', 
        to_field='cid', blank=True, null=True, on_delete=models.SET_NULL)
    receiver = models.CharField(verbose_name='收货人', max_length=32,
        blank=True, null=True)
    PAY_CHOICES = (
        (1, '全款'),
        (2, '定金'),
    )
    pay_method = models.SmallIntegerField(verbose_name='结算方式',
        choices=PAY_CHOICES)
    DELIVERY_CHOICES = (
        (1, '物流到站自提'),
        (2, '物流送货上门'),
        (3, '单车直送'),
        (4, '仓库自提'),
    )
    delivery = models.SmallIntegerField(verbose_name='运输方式',
        choices=DELIVERY_CHOICES)
    FREIGHT_CHOICES = (
        (1, '包邮'),
        (2, '到付'),
    )
    freight = models.SmallIntegerField(verbose_name='运费支付',
        choices=FREIGHT_CHOICES)
        
    '''footer'''
    remark = models.CharField(verbose_name='备注', max_length=256,
        blank=True, null=True)
    phone = models.BigIntegerField(verbose_name='电话')
    form_maker = models.ForeignKey(verbose_name='制表人', to='Personnel',
        to_field='pid',blank=True, null=True, on_delete=models.SET_NULL)
    STATUS_CHOICES = (
        (1, '未审核'),
        (2, '审核通过'),
        (3, '待付款'),
        (4, '待发货'),
        (5, '待收货'),
        (6, '待付尾款'),
        (7, '完成'),
    )
    status = models.SmallIntegerField(verbose_name='订单状态',
        choices=STATUS_CHOICES)
    def __str__(self):
        return str(self.oid)

class Include(models.Model):
    rid = models.ForeignKey(verbose_name='产品', to='Product',
        to_field='rid', on_delete=models.CASCADE)
    oid = models.ForeignKey(verbose_name='订单', to='OrderTable',
        to_field='oid', on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='数量')
    univalent = models.IntegerField(verbose_name='单价')

class Product(models.Model):
    rid = models.IntegerField(verbose_name='产品编号', unique=True)
    name = models.CharField(verbose_name='产品名称', max_length=32)
    model = models.CharField(verbose_name='规格型号', max_length=32)
    unit = models.CharField(verbose_name='单位', max_length=8)
    def __str__(self):
        return self.name

class Customer(models.Model):
    cid = models.IntegerField(verbose_name='客户编号', unique=True)
    name = models.CharField(verbose_name='客户姓名', max_length=16)
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=GENDER_CHOICES)
    phone = models.BigIntegerField(verbose_name='客户电话')
    organization = models.CharField(verbose_name='客户单位', max_length=32,
        blank=True, null=True)
    address = models.CharField(verbose_name='客户地址', max_length=64)
    job_title = models.CharField(verbose_name='客户职务', max_length=16,
        blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=64,
        blank=True, null=True)
    correspond = models.ForeignKey(verbose_name='负责经理', to='Personnel',
        to_field='pid', blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
