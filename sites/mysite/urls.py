from django.urls import path
from mysite.views import *


urlpatterns = [
    path("", index, name="home"),
    path("id<int:pk>", main, name="main"),
    path("reg", reg, name="reg"),
    path("out", loginOut, name="out"),
    path("forgot", forgot, name="forgot"),
    path("friends", viewFriends, name="friends"), #Показать список всех пользователей
    path("view/id<int:pk>", viewUser, name="viewUser"), #Показать список всех пользователей    
    path('id<int:pk>/update', UpdateUser.as_view(), name='update_user'), #Изменить свою страницу
    path('photos', photos, name='photos'),
    path('music', music, name='music'),
    path('chat', viewChat, name='chat'),
    path('dialogues', dialogues, name='dialogues'),
    path('dialogues/send<int:pk>', viewDialogues, name='viewDialogues'),
    path('validate_username', validate_username, name='validate_username'),
    path('validate_mail', validate_mail, name='validate_mail'),
]
