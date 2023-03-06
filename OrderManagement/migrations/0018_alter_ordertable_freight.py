# Generated by Django 4.0.5 on 2022-06-18 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0017_alter_customer_job_title_alter_customer_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertable',
            name='freight',
            field=models.SmallIntegerField(choices=[(1, '包邮'), (2, '到付')], verbose_name='运费支付'),
        ),
    ]
