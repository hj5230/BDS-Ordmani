# Generated by Django 4.0.5 on 2022-06-15 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0007_alter_ordertable_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertable',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderManagement.personnel', to_field='pid', verbose_name='业务经理'),
        ),
    ]
