# Generated by Django 3.0.8 on 2020-08-01 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200801_1138'),
        ('images', '0010_auto_20200801_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_profile', to='account.Profile'),
        ),
    ]
