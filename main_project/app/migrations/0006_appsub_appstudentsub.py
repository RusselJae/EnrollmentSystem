# Generated by Django 5.1.3 on 2024-11-29 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_appcsstudents_year_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_code', models.CharField(max_length=50)),
                ('sub_name', models.CharField(max_length=50)),
                ('lab_units', models.IntegerField()),
                ('lec_units', models.IntegerField()),
            ],
            options={
                'db_table': 'app_sub',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AppStudentSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub1', models.CharField(blank=True, max_length=100, null=True)),
                ('sub2', models.CharField(blank=True, max_length=100, null=True)),
                ('sub3', models.CharField(blank=True, max_length=100, null=True)),
                ('sub4', models.CharField(blank=True, max_length=100, null=True)),
                ('sub5', models.CharField(blank=True, max_length=100, null=True)),
                ('sub6', models.CharField(blank=True, max_length=100, null=True)),
                ('sub7', models.CharField(blank=True, max_length=100, null=True)),
                ('sub8', models.CharField(blank=True, max_length=100, null=True)),
                ('sub9', models.CharField(blank=True, max_length=100, null=True)),
                ('student_number', models.ForeignKey(db_column='student_number', on_delete=django.db.models.deletion.DO_NOTHING, to='app.appitstudents')),
            ],
            options={
                'db_table': 'app_student_sub',
                'managed': True,
            },
        ),
    ]
