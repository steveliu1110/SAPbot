# Generated by Django 4.2.16 on 2024-12-06 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0007_alter_chatsession_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='session_id',
            field=models.CharField(default='a1ecfe90-9339-4bbd-b3a1-625d4dabbd0d', help_text='Unique identifier for the session', max_length=100),
        ),
    ]
