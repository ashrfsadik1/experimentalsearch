# Generated by Django 3.1 on 2024-06-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20240605_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userdegree',
            field=models.IntegerField(default=1),
        ),
    ]
