# Generated by Django 5.0 on 2024-01-16 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_message_deletable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='deletable',
            field=models.BooleanField(default=False),
        ),
    ]
