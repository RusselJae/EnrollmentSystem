# Generated by Django 5.1.3 on 2024-11-26 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_appcsstudents_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appcsstudents',
            name='specialization',
        ),
        migrations.RemoveField(
            model_name='appitstudents',
            name='track',
        ),
    ]