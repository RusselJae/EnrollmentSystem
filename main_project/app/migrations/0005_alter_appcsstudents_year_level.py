# Generated by Django 5.1.3 on 2024-11-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_appcsstudents_specialization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcsstudents',
            name='year_level',
            field=models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year'), ('5', '5th Year')], max_length=50),
        ),
    ]
