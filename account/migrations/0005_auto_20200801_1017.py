# Generated by Django 3.0.8 on 2020-08-01 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='avatar_image',
        ),
    ]
