# Generated by Django 4.2.2 on 2023-07-11 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(default=None, max_length=255, unique=True),
        ),
    ]
