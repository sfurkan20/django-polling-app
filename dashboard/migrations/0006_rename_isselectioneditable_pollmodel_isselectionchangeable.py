# Generated by Django 4.0.5 on 2022-08-01 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_pollmodel_isselectioneditable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pollmodel',
            old_name='isSelectionEditable',
            new_name='isSelectionChangeable',
        ),
    ]
