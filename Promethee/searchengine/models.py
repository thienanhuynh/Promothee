# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import connection, models
from django import forms


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_firstnames = models.TextField(blank=True, null=True)
    author_initials = models.TextField(blank=True, null=True)
    author_lastname = models.TextField()
    country_code = models.TextField(blank=True, null=True)
    affiliation = models.TextField(blank=True, null=True)
    author_email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Author'
    def __str__(self):
        return self.name


class AuthorReference(models.Model):
    author = models.OneToOneField(Author, models.DO_NOTHING, primary_key=True)  # The composite primary key (author_id, reference_id) found, that is not supported. The first column is selected.
    reference = models.ForeignKey('Reference', models.DO_NOTHING)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Author_Reference'
    def __str__(self):
        return self.name


class Country(models.Model):
    country_code = models.TextField(primary_key=True)
    population_in_millions = models.IntegerField(blank=True, null=True)
    continent = models.TextField()
    researchers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Country'
    def __str__(self):
        return self.name


class CountryAuthor(models.Model):
    country_code = models.OneToOneField(Country, models.DO_NOTHING, db_column='country_code', primary_key=True)  # The composite primary key (country_code, author_id) found, that is not supported. The first column is selected.
    author = models.ForeignKey(Author, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Country_Author'
    def __str__(self):
        return self.name


class Errors(models.Model):
    error_id = models.AutoField(primary_key=True)
    country = models.TextField()
    authors = models.TextField()
    year = models.IntegerField()
    title = models.TextField()
    publisher = models.TextField()
    volume_number = models.TextField(blank=True, null=True)
    pages = models.TextField(blank=True, null=True)
    doc_type = models.TextField()
    keywords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Errors'
    def __str__(self):
        return self.name


class Genre(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword = models.TextField()

    class Meta:
        managed = False
        db_table = 'Genre'
    def __str__(self):
        return self.name


class GenreReference(models.Model):
    keyword = models.OneToOneField(Genre, models.DO_NOTHING, primary_key=True)  # The composite primary key (keyword_id, reference_id) found, that is not supported. The first column is selected.
    reference = models.ForeignKey('Reference', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Genre_Reference'
    def __str__(self):
        return self.name


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'Publisher'
    def __str__(self):
        return self.name


class Reference(models.Model):
    reference_id = models.AutoField(primary_key=True)
    title = models.TextField()
    publisher_reference = models.ForeignKey(Publisher, models.DO_NOTHING, db_column='publisher_reference', blank=True, null=True, related_name='references')
    isbn_issn = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()
    volume = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    pages = models.TextField(blank=True, null=True)
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'Reference'
    def __str__(self):
        return self.title


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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

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
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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
