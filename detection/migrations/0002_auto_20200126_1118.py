# Generated by Django 2.1.5 on 2020-01-26 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bullycomments',
            old_name='name',
            new_name='vid',
        ),
    ]
