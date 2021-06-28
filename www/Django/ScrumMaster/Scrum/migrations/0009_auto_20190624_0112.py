# Generated by Django 2.1.7 on 2019-06-24 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scrum', '0008_scrumproject_to_clear_tft'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrumchatmessage',
            name='profile_picture',
            field=models.TextField(default='prof_pic'),
        ),
        migrations.AddField(
            model_name='scrumprojectrole',
            name='slack_email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='scrumprojectrole',
            name='slack_profile_picture',
            field=models.TextField(blank=True, default='https://secure.gravatar.com/avatar/8ca9b9d6ee37371cba9ee9362cdbbc9b.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0005-512.png', null=True),
        ),
        migrations.AddField(
            model_name='scrumprojectrole',
            name='slack_user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='scrumprojectrole',
            name='slack_username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
