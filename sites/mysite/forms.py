from .models import *
from django.forms import ModelForm, FileInput, TextInput, DateInput, NumberInput, ChoiceField, Textarea, Select, ValidationError



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


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Пол не указан'

    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'birthdate', 'gender', 'hometown', 'fav_music', 'fav_movies', 'fav_quotes', 'ciggar', 'alco', 'religion', 'about', 'plink', 'telegram', 'instagram', 'phone', 'email']

        widgets = {
            "avatar": FileInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "first_name": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "last_name": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "birthdate": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "gender": Select(attrs={
                'class': 'change_profile_form_item',   
                }),
            "hometown": TextInput(attrs={
                'class': 'change_profile_form_item',   
                }),
            "fav_music": TextInput(attrs={
                'class': 'change_profile_form_item',   
                }),
            "fav_movies": TextInput(attrs={
                'class': 'change_profile_form_item',   
                }),
            "fav_quotes": TextInput(attrs={
                'class': 'change_profile_form_item',   
                }),
            "ciggar": Select(attrs={
                'class': 'change_profile_form_item',   
                }),
            "alco": Select(attrs={
                'class': 'change_profile_form_item',   
                }),
            "religion": Select(attrs={
                'class': 'change_profile_form_item',   
                }),
            "about": Textarea(attrs={
                'cols': 60,
                'rows': 13,
                'class': 'change_profile_form_item',   
                }),
            "plink": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "telegram": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "instagram": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "phone": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
            "email": TextInput(attrs={
                'class': 'change_profile_form_item',
                }),
        }

class UserPhotosForm(ModelForm):
    class Meta:
        model = UserPhotos
        fields = ['content', 'img']

        widgets = {
            "content": TextInput(attrs={
                'placeholder':'Описание',
            }),
            "img": FileInput(attrs={
                'style': 'display:none',
            })
            }
        
        
class UserMusicForm(ModelForm):
    class Meta:
        model = UserMusic
        fields = ['title', 'song']

        widgets = {
            "title": TextInput(attrs={
                'placeholder':'Название песни',
            }),
            "song": FileInput(attrs={
                'style': 'display:none',
                'accept': 'audio/mp3',
                'preload':'auto',
            })
            }
        

class ChatForm(ModelForm):
    class Meta:
        model = AllChat
        fields = ['msg', 'msg_img']

        widgets = {
            "msg": TextInput(attrs={
                'placeholder': 'Введите ваше сообщение'
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
                'placeholder': 'Введите ваше сообщение'
            }),
            "private_img": FileInput(attrs={
                'style': 'display:none',
            })
            }