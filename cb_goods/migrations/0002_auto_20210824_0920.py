# Generated by Django 3.0 on 2021-08-24 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cb_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='gtitle',
            field=models.CharField(max_length=100),
        ),
    ]
