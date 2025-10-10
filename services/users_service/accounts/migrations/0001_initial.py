from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Permission Code')),
                ('name', models.CharField(max_length=100, verbose_name='Permission Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Право доступа',
                'verbose_name_plural': 'Права доступа',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Role Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Username')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('registered_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Registered At')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='users', to='accounts.role', verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='users', to='accounts.permission', verbose_name='Permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
