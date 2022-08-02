# Generated by Django 4.0.5 on 2022-08-02 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_uservoteregistry_ipvoteregistry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollmodel',
            name='createdBy',
        ),
        migrations.RemoveField(
            model_name='uservoteregistry',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='uservoteregistry',
            name='user',
        ),
        migrations.DeleteModel(
            name='IPVoteRegistry',
        ),
        migrations.DeleteModel(
            name='PollModel',
        ),
        migrations.DeleteModel(
            name='UserVoteRegistry',
        ),
    ]
