# Generated by Django 5.0.6 on 2024-09-02 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0010_remove_member_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('normal_user', 'Normal User'), ('volunteer_team', 'Volunteer Team')], default='volunteer_team', max_length=20),
        ),
    ]
