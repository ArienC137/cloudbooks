# Generated by Django 3.0 on 2021-08-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cb_star', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='starinfo',
            name='sdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
