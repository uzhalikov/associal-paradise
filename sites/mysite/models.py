from django.db import models
from django.contrib.auth.admin import User
from django.forms import ValidationError


class UserProfile(models.Model):
    ciggar_choices = [
        ('p', 'Положительное'),
        ('n', 'Отрицательное'),
    ]
    alco_choices = [
        ('p', 'Положительное'),
        ('n', 'Отрицательное'),
    ]
    gender_choices = [
        ('m', 'Мужской'),
        ('w', 'Женский'),
    ]
    religion_choices = [
        ('chr', 'Христианство'),
        ('isl', 'Ислам'),
        ('ind', 'Индуизм'),
        ('bdm', 'Буддизм'),
        ('iud', 'Иудаизм'),
        ('atm', 'Атеизм'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="mysite/static/images/personal_photos/", blank=True, verbose_name='Аватарка',
        default='mysite/static/images/icons/none_avatar.png')
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, blank=True, null=True, choices=gender_choices, verbose_name='Пол')
    hometown = models.CharField(max_length=30, blank=True, null=True, verbose_name='Родной город')

    fav_music = models.CharField(max_length=30, blank=True, null=True, verbose_name='Любимая музыка')
    fav_movies = models.CharField(max_length=30, blank=True, null=True, verbose_name='Любимые фильмы')
    fav_quotes = models.CharField(max_length=30, blank=True, null=True, verbose_name='Любимые цитаты')
    ciggar = models.CharField(max_length=1, blank=True, null=True, choices=ciggar_choices,
                              verbose_name='Отношение к курению')
    alco = models.CharField(max_length=1, blank=True, null=True, choices=alco_choices,
                            verbose_name='Отношение к алкоголю')
    religion = models.CharField(max_length=3, blank=True, null=True, choices=religion_choices, verbose_name='Религия')
    about = models.TextField(max_length=150, blank=True, null=True, verbose_name='О себе')

    plink = models.CharField(max_length=10, blank=True, null=True, verbose_name='Короткая ссылка')
    telegram = models.CharField(max_length=30, blank=True, null=True, verbose_name='Telegram')
    instagram = models.CharField(max_length=30, blank=True, null=True, verbose_name='Instagram')
    email = models.EmailField(max_length=30, blank=True, null=True, verbose_name='Почта')
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name='Телефон')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return f'/id{self.id}'

    class Meta:
        verbose_name_plural = 'Информация о пользователях'


class UserWall(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    user_recipient_id = models.TextField(max_length=1000, blank=True, null=True)
    content = models.TextField(max_length=1000, blank=True, null=True)
    img = models.ImageField(
        upload_to="mysite/static/images/userwall_photos/", blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.content == '' and self.img == '':
            raise ValidationError({'img': ('Упс. Нужно что-то ввести :)')})

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Информация со стен пользователей'


class HaveDialog(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    user_recipient_id = models.TextField(max_length=1000)
    last_message = models.TextField(max_length=1000)
    last_sender = models.TextField(max_length=1000)
    status_message = models.BooleanField(default=False)
    time_update = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Наличие диалога'


class Dialogs(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    user_recipient_id = models.TextField(max_length=1000, blank=True, null=True)
    private_message = models.TextField(max_length=1000, blank=True, null=True)
    was_read = models.BooleanField(blank=True, null=True, default=False)
    private_img = models.ImageField(
        upload_to="mysite/static/images/dialog_photos/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.private_message == '' and self.private_img == '':
            raise ValidationError({'private_message': ('Упс. Нужно что-то ввести :)')})

    def __str__(self):
        return self.private_message

    class Meta:
        verbose_name_plural = 'Состав диалога'


class UserPhotos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Название')
    img = models.ImageField(
        upload_to="mysite/static/images/personal_photos/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.img == '':
            raise ValidationError({'img': ('Нужно добавить изображение.')})

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Фотографии пользователей'


class UserMusic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=200, blank=True, null=True)
    song = models.FileField(
        upload_to="mysite/static/music/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.title == '' and self.song == '':
            raise ValidationError({'title': ('Упс. Нужно что-то ввести :)')})
        elif self.song == '':
            raise ValidationError({'title': ('Упс. Нужно что-то ввести :)')})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Музыка'


class FriendsList(models.Model):
    from_user = models.TextField(max_length=100)
    to_user = models.TextField(max_length=100)
    friends = models.TextField(max_length=1, default=0)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Друзья'


class AllChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField(max_length=999999, verbose_name='', blank=True, null=True)
    msg_time_create = models.DateTimeField(auto_now_add=True)
    msg_time_update = models.DateTimeField(auto_now=True)
    msg_img = models.ImageField(
        upload_to="mysite/static/images/chat_photos/", blank=True, verbose_name='')
    
    def clean(self):
        if self.msg == '' and self.msg_img == '':
            raise ValidationError({'msg': ('Упс. Нужно что-то ввести :)')})

    class Meta:
        verbose_name_plural = 'Чат'
