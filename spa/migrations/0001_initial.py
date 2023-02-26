# Generated by Django 4.1.7 on 2023-02-22 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=35, null=True, verbose_name='название курса')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='описание курса')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(blank=True, max_length=35, null=True, verbose_name='пользователь')),
                ('date_of_payment', models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')),
                ('object_of_payment', models.CharField(blank=True, max_length=45, null=True, verbose_name='оплаченый курс или урок')),
                ('sum_of_payment', models.IntegerField(blank=True, null=True, verbose_name='сумма оплаты')),
                ('form_of_payment', models.CharField(blank=True, max_length=45, null=True, verbose_name='способ оплаты наличные или перевод')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=35, null=True, verbose_name='название урока')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='картинка к уроку')),
                ('description', models.CharField(blank=True, max_length=350, null=True, verbose_name='описание урока')),
                ('reference', models.CharField(blank=True, max_length=55, null=True, verbose_name='ссылка на видео')),
                ('smth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='smthin', to='spa.course')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=240, unique=True)),
                ('password', models.CharField(max_length=240)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
