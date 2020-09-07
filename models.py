# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
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
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class Hospital(models.Model):
    h_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=512, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    username = models.CharField(max_length=15)
    passwd = models.CharField(max_length=50)
    mild_left = models.IntegerField(blank=True, null=True)
    severe_left = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    city = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'hospital'


class Patient(models.Model):
    p_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(Hospital, models.DO_NOTHING)
    no = models.CharField(max_length=64)
    tel = models.CharField(max_length=20)
    username = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient'


class Pstatus(models.Model):
    p = models.OneToOneField(Patient, models.DO_NOTHING, primary_key=True)
    status = models.IntegerField()
    day = models.DateField()

    class Meta:
        managed = False
        db_table = 'pstatus'
        unique_together = (('p', 'status'),)


class Supplies(models.Model):
    h = models.OneToOneField(Hospital, models.DO_NOTHING, primary_key=True)
    n95 = models.IntegerField()
    surgeon = models.IntegerField()
    ventilator = models.IntegerField()
    clothe = models.IntegerField()
    glasses = models.IntegerField()
    alcohol = models.IntegerField()
    pants = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supplies'


class Track(models.Model):
    p = models.OneToOneField(Patient, models.DO_NOTHING, primary_key=True)
    date_time = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    district = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track'
        unique_together = (('p', 'date_time'),)
