# Generated by Django 4.2.16 on 2024-12-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_chatsession_name_alter_chatsession_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='name',
            field=models.CharField(default='Empty Session', help_text='Unique name for the session', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='session_id',
            field=models.CharField(default='5c8601a1-f6ab-4c24-b17c-14212b9d1655', help_text='Unique identifier for the session', max_length=100, unique=True),
        ),
    ]