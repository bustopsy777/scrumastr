# Generated by Django 2.1.7 on 2019-05-20 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scrum', '0006_scrumgoal_days_failed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrumgoalhistory',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='scrumsprint',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='scrumgoal',
            name='push_id',
            field=models.CharField(default='Null Value', max_length=10),
        ),
    ]
