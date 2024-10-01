# Generated by Django 5.0.6 on 2024-09-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_member_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]