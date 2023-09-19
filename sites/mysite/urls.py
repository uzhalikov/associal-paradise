from django.urls import path
from mysite.views import *


urlpatterns = [
    path("", index, name="home"),
    path("id<int:pk>", main, name="main"),
    path("reg/", reg, name="reg"),
    path("out/", loginOut, name="out"),
    path("forgot/", forgot, name="forgot"),
    path("users", AllUsers.as_view(), name="users"), #Показать список всех пользователей
    path("view/id<int:pk>", viewUser, name="viewUser"), #Показать список всех пользователей    
    #path('view/id<int:pk>', ViewUser.as_view(), name='view_user'),    
    path('id<int:pk>/update', UpdateUser.as_view(), name='update_user'), #Изменить свою страницу
    path('photos', photos, name='photos'),
    path('music', music, name='music'),
    path('chat', viewChat, name='chat'),
    path('dialogues', dialogues, name='dialogues'),
    path('dialogues/send<int:pk>', viewDialogues, name='viewDialogues'),
]
