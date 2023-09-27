from .models import *
from django.forms import ModelForm, FileInput, TextInput, DateInput, NumberInput, ChoiceField, Textarea, DateTimeInput


class UserWallForm(ModelForm):
    class Meta:
        model = UserWall
        fields = ['content', 'img']
        widgets = {
            "content": TextInput(attrs={
                'placeholder': 'Что нового?',
            }),
            'img': FileInput(attrs={
                'style': 'display:none',
            }),
        }


class DeleteFriendForm(ModelForm):
    class Meta:
        model = FriendsList
        fields = ['from_user', 'to_user']
        widgets = {
            "from_user": TextInput(attrs={
                'type': 'hidden',
            }),
            'to_user': TextInput(attrs={
                'type': 'hidden',
            }),
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'birthdate', 'gender', 'hometown', 'fav_music', 'fav_movies',
                  'fav_quotes', 'ciggar', 'alco', 'religion', 'about', 'plink', 'telegram', 'instagram', 'phone',
                  'email']
        widgets = {
            "about": Textarea(attrs={
                'placeholder': 'Максимум 150 символов.',
            }),
            "avatar": FileInput(attrs={
                'style': 'display: none',
            }),
            "birthdate": DateInput(attrs={
                'type': 'date'
            }),
        }


class UserPhotosForm(ModelForm):
    class Meta:
        model = UserPhotos
        fields = ['content', 'img']

        widgets = {
            "content": TextInput(attrs={
                'placeholder': 'Описание',
                'autofocus': True,
            }),
            "img": FileInput(attrs={
                'style': 'display: none',
            }),
        }


class UserMusicForm(ModelForm):
    class Meta:
        model = UserMusic
        fields = ['title', 'song']

        widgets = {
            "title": TextInput(attrs={
                'placeholder': 'Название песни',
                'autofocus': True,
            }),
            "song": FileInput(attrs={
                'style': 'display:none',
                'accept': 'audio/mp3',
                'preload': 'auto',
            })
        }


class ChatForm(ModelForm):
    class Meta:
        model = AllChat
        fields = ['msg', 'msg_img']

        widgets = {
            "msg": TextInput(attrs={
                'placeholder': 'Введите ваше сообщение',
                'autofocus': True,
            }),
            "msg_img": FileInput(attrs={
                'style': 'display:none',
            })
        }


class DialogsForm(ModelForm):
    class Meta:
        model = Dialogs
        fields = ['private_message', 'private_img']

        widgets = {
            "private_message": TextInput(attrs={
                'placeholder': 'Введите ваше сообщение',
                'autofocus': True,
            }),
            "private_img": FileInput(attrs={
                'style': 'display:none',
            })
        }
