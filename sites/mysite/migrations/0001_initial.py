# Generated by Django 4.2.3 on 2023-09-23 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.TextField(max_length=100)),
                ('to_user', models.TextField(max_length=100)),
                ('friends', models.TextField(default=0, max_length=1)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Друзья',
            },
        ),
        migrations.CreateModel(
            name='UserWall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_recipient_id', models.TextField(blank=True, max_length=1000, null=True)),
                ('content', models.TextField(blank=True, max_length=1000, null=True)),
                ('img', models.ImageField(blank=True, upload_to='mysite/static/images/userwall_photos/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('user_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Информация со стен пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='mysite/static/images/icons/none_avatar.png', upload_to='mysite/static/images/personal_photos/', verbose_name='Аватарка')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Фамилия')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Мужской'), ('w', 'Женский')], max_length=1, null=True, verbose_name='Пол')),
                ('hometown', models.CharField(blank=True, max_length=30, null=True, verbose_name='Родной город')),
                ('fav_music', models.CharField(blank=True, max_length=30, null=True, verbose_name='Любимая музыка')),
                ('fav_movies', models.CharField(blank=True, max_length=30, null=True, verbose_name='Любимые фильмы')),
                ('fav_quotes', models.CharField(blank=True, max_length=30, null=True, verbose_name='Любимые цитаты')),
                ('ciggar', models.CharField(blank=True, choices=[('p', 'Положительное'), ('n', 'Отрицательное')], max_length=1, null=True, verbose_name='Отношение к курению')),
                ('alco', models.CharField(blank=True, choices=[('p', 'Положительное'), ('n', 'Отрицательное')], max_length=1, null=True, verbose_name='Отношение к алкоголю')),
                ('religion', models.CharField(blank=True, choices=[('chr', 'Христианство'), ('isl', 'Ислам'), ('ind', 'Индуизм'), ('bdm', 'Буддизм'), ('iud', 'Иудаизм'), ('atm', 'Атеизм')], max_length=3, null=True, verbose_name='Религия')),
                ('about', models.TextField(blank=True, max_length=500, null=True, verbose_name='О себе')),
                ('plink', models.CharField(blank=True, max_length=10, null=True, verbose_name='Короткая ссылка')),
                ('telegram', models.CharField(blank=True, max_length=30, null=True, verbose_name='Telegram')),
                ('instagram', models.CharField(blank=True, max_length=30, null=True, verbose_name='Instagram')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Информация о пользователях',
            },
        ),
        migrations.CreateModel(
            name='UserPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Название')),
                ('img', models.ImageField(blank=True, upload_to='mysite/static/images/personal_photos/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Фотографии пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=200, null=True)),
                ('song', models.FileField(blank=True, upload_to='mysite/static/music/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Музыка пользователей',
            },
        ),
        migrations.CreateModel(
            name='HaveDialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_recipient_id', models.TextField(max_length=1000)),
                ('last_message', models.TextField(max_length=1000)),
                ('last_sender', models.TextField(max_length=1000)),
                ('status_message', models.BooleanField(default=False)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('user_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Наличие диалога',
            },
        ),
        migrations.CreateModel(
            name='Dialogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_recipient_id', models.TextField(blank=True, max_length=1000, null=True)),
                ('private_message', models.TextField(blank=True, max_length=1000, null=True)),
                ('was_read', models.BooleanField(blank=True, default=False, null=True)),
                ('private_img', models.ImageField(blank=True, upload_to='mysite/static/images/dialog_photos/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('user_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Состав диалога',
            },
        ),
        migrations.CreateModel(
            name='AllChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(blank=True, max_length=999999, null=True, verbose_name='')),
                ('msg_time_create', models.DateTimeField(auto_now_add=True)),
                ('msg_time_update', models.DateTimeField(auto_now=True)),
                ('msg_img', models.ImageField(blank=True, upload_to='mysite/static/images/chat_photos/', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Чат',
            },
        ),
    ]
