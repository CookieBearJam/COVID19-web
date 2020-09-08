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
    # 在这里面进行xml文件的解析和字典的初始化

    h_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='名字')
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name='地址')
    tel = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    contact = models.CharField(max_length=10, blank=True, null=True, verbose_name='联系人')
    username = models.CharField(max_length=15, verbose_name='用户名')
    passwd = models.CharField(max_length=50, verbose_name='登录密码')
    mild_left = models.IntegerField(blank=True, null=True, verbose_name='轻症剩余')
    severe_left = models.IntegerField(blank=True, null=True, verbose_name='重症剩余')
    province = models.CharField(max_length=10, verbose_name='省')  # 只修改了显示的名字
    city = models.CharField(max_length=10, verbose_name='市')
    district = models.CharField(max_length=10, verbose_name='区/县')

    class Meta:
        managed = False
        db_table = 'hospital'
        # verbose_name_plural = '医院'
        verbose_name = '医院'


def __str__(self):
    return self.name


class Patient(models.Model):
    p_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(Hospital, models.DO_NOTHING)
    no = models.CharField(max_length=64, verbose_name='病案号')
    tel = models.CharField(max_length=20, verbose_name='电话号')
    username = models.CharField(max_length=64, blank=True, null=True, verbose_name='用户名')
    status = models.IntegerField(verbose_name='状态')

    class Meta:
        managed = False
        db_table = 'patient'
        verbose_name_plural = verbose_name = '病人信息'

    def __str__(self):
        return self.name


class Pstatus(models.Model):
    p = models.OneToOneField(Patient, models.DO_NOTHING, primary_key=True)
    status = models.IntegerField(verbose_name='状态')
    day = models.DateField(verbose_name='日期')

    class Meta:
        managed = False
        db_table = 'pstatus'
        unique_together = (('p', 'status'),)
        verbose_name_plural = verbose_name = '病人状态'

    def __str__(self):
        return self.name


class Supplies(models.Model):
    h = models.OneToOneField(Hospital, models.DO_NOTHING, primary_key=True)
    n95 = models.IntegerField(default=0, verbose_name='N95口罩缺少数量/个')
    surgeon = models.IntegerField(default=0, verbose_name='医用外科口罩欠缺量/个')
    ventilator = models.IntegerField(default=0, verbose_name='呼吸机欠缺量/台')
    clothe = models.IntegerField(default=0, verbose_name='防护服欠缺量/件')
    glasses = models.IntegerField(default=0, verbose_name='护目镜欠缺量')
    alcohol = models.IntegerField(default=0, verbose_name='酒精欠缺量/瓶')
    pants = models.IntegerField(default=0, verbose_name='安心裤欠缺量/条')

    class Meta:
        managed = False
        db_table = 'supplies'
        verbose_name_plural = verbose_name = '物资'

    def __str__(self):
        return self.name


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
        verbose_name_plural = verbose_name = '病人轨迹'

    def __str__(self):
        return self.name
