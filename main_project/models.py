# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppCsChecklist(models.Model):
    student_number = models.IntegerField(db_column='student number', unique=True)  # Field renamed to remove unsuitable characters.
    gned_02 = models.DecimalField(db_column='GNED 02', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_05 = models.DecimalField(db_column='GNED 05', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_11 = models.DecimalField(db_column='GNED 11', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_50 = models.DecimalField(db_column='COSC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_21 = models.DecimalField(db_column='DCIT 21', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_22 = models.DecimalField(db_column='DCIT 22', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_1 = models.DecimalField(db_column='FITT 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_1 = models.DecimalField(db_column='NSTP 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cvsu_101 = models.DecimalField(db_column='CvSU 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_01 = models.DecimalField(db_column='GNED 01', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_03 = models.DecimalField(db_column='GNED 03', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_06 = models.DecimalField(db_column='GNED 06', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_12 = models.DecimalField(db_column='GNED 12', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_23 = models.DecimalField(db_column='DCIT 23', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_50 = models.DecimalField(db_column='ITEC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_2 = models.DecimalField(db_column='FITT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_2 = models.DecimalField(db_column='NSTP 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_04 = models.DecimalField(db_column='GNED 04', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_1 = models.DecimalField(db_column='MATH 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_55 = models.DecimalField(db_column='COSC 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_60 = models.DecimalField(db_column='COSC 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_50 = models.DecimalField(db_column='DCIT 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_24 = models.DecimalField(db_column='DCIT 24', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    insy_50 = models.DecimalField(db_column='INSY 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_3 = models.DecimalField(db_column='FITT 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_08 = models.DecimalField(db_column='GNED 08', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_14 = models.DecimalField(db_column='GNED 14', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_2 = models.DecimalField(db_column='MATH 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_65 = models.DecimalField(db_column='COSC 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_70 = models.DecimalField(db_column='COSC 70', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_25 = models.DecimalField(db_column='DCIT 25', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_55 = models.DecimalField(db_column='DCIT 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_4 = models.DecimalField(db_column='FITT 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_3 = models.DecimalField(db_column='MATH 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_75 = models.DecimalField(db_column='COSC 75', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_80 = models.DecimalField(db_column='COSC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_85 = models.DecimalField(db_column='COSC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_101 = models.DecimalField(db_column='COSC 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_26 = models.DecimalField(db_column='DCIT 26', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_65 = models.DecimalField(db_column='DCIT 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_09 = models.DecimalField(db_column='GNED 09', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_4 = models.DecimalField(db_column='MATH 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_90 = models.DecimalField(db_column='COSC 90', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_95 = models.DecimalField(db_column='COSC 95', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_106 = models.DecimalField(db_column='COSC 106', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_60 = models.DecimalField(db_column='DCIT 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_85 = models.DecimalField(db_column='ITEC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_199 = models.DecimalField(db_column='COSC 199', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_80 = models.DecimalField(db_column='ITEC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_100 = models.DecimalField(db_column='COSC 100', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_105 = models.DecimalField(db_column='COSC 105', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_111 = models.DecimalField(db_column='COSC 111', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_200a = models.DecimalField(db_column='COSC 200A', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_07 = models.DecimalField(db_column='GNED 07', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_10 = models.DecimalField(db_column='GNED 10', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_110 = models.DecimalField(db_column='COSC 110', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_200b = models.DecimalField(db_column='COSC 200B', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'app_cs_checklist'


class AppCsStudents(models.Model):
    student_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    year_level = models.CharField(max_length=50)
    section = models.IntegerField()
    status = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    soc_fee = models.CharField(max_length=100)
    date_enrolled = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()
    is_archived = models.IntegerField(blank=True, null=True)
    archived_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_cs_students'


class AppCsStudentsSub(models.Model):
    student_number = models.IntegerField(unique=True)
    sub1 = models.CharField(max_length=100)
    sub2 = models.CharField(max_length=100)
    sub3 = models.CharField(max_length=100)
    sub4 = models.CharField(max_length=100)
    sub5 = models.CharField(max_length=100)
    sub6 = models.CharField(max_length=100)
    sub7 = models.CharField(max_length=100)
    sub8 = models.CharField(max_length=100)
    sub9 = models.CharField(max_length=100)
    encoder = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_cs_students_sub'


class AppDcsAdmission(models.Model):
    student_number = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'app_dcs_admission'


class AppItChecklist(models.Model):
    student_number = models.IntegerField(db_column='student number', unique=True)  # Field renamed to remove unsuitable characters.
    gned_02 = models.DecimalField(db_column='GNED 02', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_05 = models.DecimalField(db_column='GNED 05', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_11 = models.DecimalField(db_column='GNED 11', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_50 = models.DecimalField(db_column='COSC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_21 = models.DecimalField(db_column='DCIT 21', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_22 = models.DecimalField(db_column='DCIT 22', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_1 = models.DecimalField(db_column='FITT 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_1 = models.DecimalField(db_column='NSTP 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cvsu_101 = models.DecimalField(db_column='CvSU 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_01 = models.DecimalField(db_column='GNED 01', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_03 = models.DecimalField(db_column='GNED 03', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_06 = models.DecimalField(db_column='GNED 06', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_12 = models.DecimalField(db_column='GNED 12', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_23 = models.DecimalField(db_column='DCIT 23', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_50 = models.DecimalField(db_column='ITEC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_2 = models.DecimalField(db_column='FITT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_2 = models.DecimalField(db_column='NSTP 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_04 = models.DecimalField(db_column='GNED 04', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_07 = models.DecimalField(db_column='GNED 07', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_10 = models.DecimalField(db_column='GNED 10', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_14 = models.DecimalField(db_column='GNED 14', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_55 = models.DecimalField(db_column='ITEC 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_24 = models.DecimalField(db_column='DCIT 24', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_50 = models.DecimalField(db_column='DCIT 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_3 = models.DecimalField(db_column='FITT 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_08 = models.DecimalField(db_column='GNED 08', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_25 = models.DecimalField(db_column='DCIT 25', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_60 = models.DecimalField(db_column='ITEC 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_65 = models.DecimalField(db_column='ITEC 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_55 = models.DecimalField(db_column='DCIT 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_70 = models.DecimalField(db_column='ITEC 70', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_4 = models.DecimalField(db_column='FITT 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    stat_2 = models.DecimalField(db_column='STAT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_75 = models.DecimalField(db_column='ITEC 75', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_80 = models.DecimalField(db_column='ITEC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_85 = models.DecimalField(db_column='ITEC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_90 = models.DecimalField(db_column='ITEC 90', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    insy_55 = models.DecimalField(db_column='INSY 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_26 = models.DecimalField(db_column='DCIT 26', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_60 = models.DecimalField(db_column='DCIT 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_09 = models.DecimalField(db_column='GNED 09', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_95 = models.DecimalField(db_column='ITEC 95', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_101 = models.DecimalField(db_column='ITEC 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_106 = models.DecimalField(db_column='ITEC 106', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_100 = models.DecimalField(db_column='ITEC 100', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_105 = models.DecimalField(db_column='ITEC 105', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_200a = models.DecimalField(db_column='ITEC 200A', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_65 = models.DecimalField(db_column='DCIT 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_111 = models.DecimalField(db_column='ITEC 111', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_116 = models.DecimalField(db_column='ITEC 116', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_110 = models.DecimalField(db_column='ITEC 110', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_200b = models.DecimalField(db_column='ITEC 200B', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_199 = models.DecimalField(db_column='ITEC 199', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'app_it_checklist'


class AppItStudents(models.Model):
    student_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    year_level = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    soc_fee = models.CharField(max_length=100)
    date_enrolled = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()
    is_archived = models.IntegerField(blank=True, null=True)
    archived_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_it_students'


class AppItStudentsSub(models.Model):
    student_number = models.IntegerField(unique=True)
    sub1 = models.CharField(max_length=100)
    sub2 = models.CharField(max_length=100)
    sub3 = models.CharField(max_length=100)
    sub4 = models.CharField(max_length=100)
    sub5 = models.CharField(max_length=100)
    sub6 = models.CharField(max_length=100)
    sub7 = models.CharField(max_length=100)
    sub8 = models.CharField(max_length=100)
    sub9 = models.CharField(max_length=100)
    encoder = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_it_students_sub'


class AppSub(models.Model):
    sub_code = models.CharField(max_length=50)
    sub_name = models.CharField(max_length=100)
    lab_units = models.IntegerField()
    lec_units = models.IntegerField()
    year_level = models.IntegerField()
    semester = models.IntegerField()
    prerequisite = models.CharField(max_length=200)
    cs = models.CharField(max_length=50, blank=True, null=True)
    it = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_sub'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
