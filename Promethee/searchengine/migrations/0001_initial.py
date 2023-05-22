# Generated by Django 4.2.1 on 2023-05-07 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_firstnames', models.TextField(blank=True, null=True)),
                ('author_initials', models.TextField(blank=True, null=True)),
                ('author_lastname', models.TextField()),
                ('country_code', models.TextField(blank=True, null=True)),
                ('affiliation', models.TextField(blank=True, null=True)),
                ('author_email', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
                ('first_name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_code', models.TextField(primary_key=True, serialize=False)),
                ('population_in_millions', models.IntegerField(blank=True, null=True)),
                ('continent', models.TextField()),
                ('researchers', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
                ('action_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('error_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.TextField()),
                ('authors', models.TextField()),
                ('year', models.IntegerField()),
                ('title', models.TextField()),
                ('publisher', models.TextField()),
                ('volume_number', models.TextField(blank=True, null=True)),
                ('pages', models.TextField(blank=True, null=True)),
                ('doc_type', models.TextField()),
                ('keywords', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Errors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('keyword_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.TextField()),
            ],
            options={
                'db_table': 'Genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('publisher_id', models.AutoField(primary_key=True, serialize=False)),
                ('publisher_name', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'Publisher',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('reference_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('isbn_issn', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('volume', models.TextField(blank=True, null=True)),
                ('number', models.TextField(blank=True, null=True)),
                ('pages', models.TextField(blank=True, null=True)),
                ('type', models.TextField()),
            ],
            options={
                'db_table': 'Reference',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthorReference',
            fields=[
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='searchengine.author')),
                ('position', models.IntegerField()),
            ],
            options={
                'db_table': 'Author_Reference',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CountryAuthor',
            fields=[
                ('country_code', models.OneToOneField(db_column='country_code', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='searchengine.country')),
            ],
            options={
                'db_table': 'Country_Author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GenreReference',
            fields=[
                ('keyword', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='searchengine.genre')),
            ],
            options={
                'db_table': 'Genre_Reference',
                'managed': False,
            },
        ),
    ]
