# Generated by Django 4.0.5 on 2022-07-07 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0018_alter_ordertable_freight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertable',
            name='delivery',
            field=models.SmallIntegerField(choices=[(1, '物流到站自提'), (2, '物流送货上门'), (3, '单车直送'), (4, '仓库自提')], verbose_name='运输方式'),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='pay_method',
            field=models.SmallIntegerField(choices=[(1, '全款'), (2, '定金')], verbose_name='结算方式'),
        ),
    ]
