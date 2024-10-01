# Generated by Django 5.0.6 on 2024-08-31 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_alter_member_is_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='role',
            field=models.CharField(choices=[('normal_user', 'Normal User'), ('volunteer_team', 'Volunteer Team')], default='normal_user', max_length=20),
        ),
    ]
