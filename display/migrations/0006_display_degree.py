# Generated by Django 3.1 on 2024-06-01 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0005_display_isyoutube'),
    ]

    operations = [
        migrations.CreateModel(
            name='Display_Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displaydegree', models.IntegerField(default=0)),
                ('display', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='display.display')),
            ],
        ),
    ]
