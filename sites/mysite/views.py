from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import UpdateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import *
from .models import *
from datetime import datetime
import os
import re

CURR_DIR = os.getcwd().replace('\\', '/') + '/' #Текущая директория


def getAuthUser(request):
    return request.session.get('is_auth', False)


def getUser(userid):
    return UserProfile.objects.get(user_id=userid)


def calculation_unread(messages, userid):
    msg = 0
    for i in messages:
        if i.status_message == 0 and int(i.last_sender) != userid:
            msg += 1
    return msg


def getAllMessages(userid):
    allMsg = HaveDialog.objects.raw(
        f'select 1 as id, up.first_name as name_sender, up2.first_name as name_recipient, hd.time_update, hd.last_sender, up3.first_name as name_last_sender, hd.user_recipient_id, hd.user_sender_id, hd.status_message, up.avatar, hd.last_message from mysite_havedialog hd join mysite_userprofile up on up.user_id = hd.user_sender_id join mysite_userprofile up2 on up2.user_id = hd.user_recipient_id join mysite_userprofile up3 on up3.user_id = hd.last_sender where hd.user_recipient_id = {userid} order by hd.time_update desc')
    return allMsg


@login_required(login_url='home')
def viewFriends(request):
    userid = getAuthUser(request)
    personal_data = getUser(userid)
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    friends = FriendsList.objects.raw(
            f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.to_user = up.user_id WHERE fl.from_user = {userid} and fl.friends = 1')
    followers = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {userid} and fl.friends = 0')

    data = {
        'userid': userid,
        'personal_data': personal_data,
        'allDialogues': allDialogues,
        'unread_messages': unread_messages,     
        'friends': friends,
        'followers': followers,
        'len_followers': len(followers),
    }

    if request.method == 'POST':
        form = request.POST
        data['find_user'] = UserProfile.objects.filter(first_name__contains=form['search_friend'])
    return render(request, 'friends.html', data)

class UpdateUser(UpdateView):
    model = UserProfile
    template_name = 'change.html'
    form_class = UserProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userid'] = getAuthUser(self.request)
        context['personal_data'] = getUser(context['userid'])
        return context


def index(request):
    err = ''
    userid = getAuthUser(request)
    if userid != False:
        return redirect(f'/id{userid}')
    else:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST["log"], password=request.POST['psw'])
            if user is not None:
                login(request, user)
                request.session['is_auth'] = user.id
                active_user = User.objects.get(id=user.id)
                active_user.last_login = datetime.now()
                active_user.save(update_fields=['last_login'])
                return redirect(f'/id{user.id}')
            else:
                err = "Ошибка! Данного пользователя не существует!"
        return render(request, 'index.html', {'err': err})


def reg(request):
    congr = ''
    #userid = getAuthUser(request)
    #if userid != False:
    #    return redirect(f'/id{userid}')
    #else:
    #    if request.method == 'POST':
    #        data = request.POST
    #        User.objects.create_user(username=data['username'], email=data['email'], password=data['password'],
    #                                 first_name=data['first_name'], last_name=data['last_name'])
    #        new_user_id = User.objects.get(username=data['username'])
    #        UserProfile.objects.create(user_id=new_user_id.id, first_name=new_user_id.first_name,
    #                                   last_name=new_user_id.last_name, email=new_user_id.email)
    #        congr = 'Поздравляем! Вы успешно зарегистрировались и можете авторизоваться в системе.'
    return render(request, 'reg.html', {'congr': congr})


@login_required(login_url='home')
def dialogues(request):
    userid = getAuthUser(request)
    personal_data = getUser(userid)
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)

    data = {
        'unread_messages': unread_messages,
        'userid': userid,
        'allDialogues': allDialogues,
        'personal_data': personal_data
    }
    if request.method == "POST":
        delete_dialog = request.POST
        HaveDialog.objects.filter(user_recipient_id=userid, user_sender_id=delete_dialog['sender_id']).delete()
        HaveDialog.objects.filter(user_recipient_id=delete_dialog['sender_id'], user_sender_id=userid).delete()
        Dialogs.objects.filter(user_recipient_id=userid, user_sender_id=delete_dialog['sender_id']).delete()
        Dialogs.objects.filter(user_recipient_id=delete_dialog['sender_id'], user_sender_id=userid).delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'dialogues.html', data)


@login_required(login_url='home')
def viewDialogues(request, pk):
    clean_id = re.findall(r'\d+', request.path)
    userid = getAuthUser(request)
    personal_data = getUser(userid)
    form = DialogsForm()
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    dialogues = Dialogs.objects.raw(
        f'select * from mysite_dialogs di join mysite_userprofile up on di.user_sender_id = up.user_id where di.user_sender_id = {clean_id[0]} and di.user_recipient_id = {userid} or di.user_sender_id = {userid} and di.user_recipient_id = {clean_id[0]} order by di.time_create desc')
    user_info = UserProfile.objects.raw(
        f'select * from mysite_userprofile up join auth_user au on au.id = up.user_id where up.user_id = {clean_id[0]}')
    try:
        dialogObj = HaveDialog.objects.get(user_sender_id=clean_id[0], user_recipient_id=userid,
                                           last_sender=clean_id[0])
        dialogObj.status_message = 1
        if dialogObj:
            dialogObj2 = HaveDialog.objects.get(user_sender_id=userid, user_recipient_id=clean_id[0],
                                                last_sender=clean_id[0])
            dialogObj2.status_message = 1
            dialogObj2.save()
        dialogObj.save()
    except:
        pass

    data = {
        'allDialogues': allDialogues,
        'unread_messages': unread_messages,
        'userid': userid,
        'dialogues': dialogues,
        'form': form,
        'user_info': user_info,
        'personal_data': personal_data
    }
    if request.method == "POST":
        form = DialogsForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_sender_id = userid
            form.user_recipient_id = clean_id[0]
            checkDialog = HaveDialog.objects.filter(user_sender_id=userid, user_recipient_id=clean_id[0])
            if not checkDialog:
                HaveDialog.objects.create(user_sender_id=userid, user_recipient_id=clean_id[0],
                                          last_message=form.private_message, last_sender=userid,
                                          time_update=datetime.now())
                HaveDialog.objects.create(user_sender_id=clean_id[0], user_recipient_id=userid,
                                          last_message=form.private_message, last_sender=userid,
                                          time_update=datetime.now())
            else:
                firstObj = HaveDialog.objects.get(user_sender_id=userid, user_recipient_id=clean_id[0])
                secObj = HaveDialog.objects.get(user_sender_id=clean_id[0], user_recipient_id=userid)
                if form.private_message:
                    firstObj.last_message = form.private_message
                    secObj.last_message = form.private_message
                else:
                    firstObj.last_message = 'pictures'
                    secObj.last_message = 'pictures'

                firstObj.status_message = False
                firstObj.last_sender = userid
                firstObj.time_update = datetime.now()
                secObj.status_message = False
                secObj.last_sender = userid
                secObj.time_update = datetime.now()
                firstObj.save()
                secObj.save()
            form.save()
    return render(request, 'viewDialogues.html', data)


@login_required(login_url='home')
def viewChat(request):
    userid = getAuthUser(request)
    personal_data = getUser(userid) 
    form = ChatForm()
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    allMessages = AllChat.objects.raw(
        'SELECT * FROM MYSITE_ALLCHAT CH JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = CH.USER_ID ORDER BY CH.MSG_TIME_CREATE DESC')[:160]
    paginator = Paginator(allMessages, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'unread_messages': unread_messages,
        'userid': userid,
        'form': form,
        'allMessages': allMessages,
        'personal_data': personal_data,
        'page_obj': page_obj,
    }

    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = userid
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            try:
                message_del = request.POST
                AllChat.objects.get(id=message_del['message_id']).delete()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            except:
                pass
    return render(request, 'chat.html', data)


@login_required(login_url='home')
def photos(request):
    userid = getAuthUser(request)
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    personal_data = getUser(userid)
    userPhoto = UserPhotos.objects.filter(user_id=userid).order_by('-time_create')
    form = UserPhotosForm()
    data = {
        'userid': userid,
        'allDialogues': allDialogues,
        'unread_messages': unread_messages,
        'userPhoto': userPhoto,
        'form': form,
        'personal_data': personal_data
    }
    if request.method == "POST":
        form = UserPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = userid
            form.save()
        else:
            delete_photo_form = request.POST
            delete_photo = UserPhotos.objects.get(id=delete_photo_form['photo_id'])
            os.remove(f'{CURR_DIR}{delete_photo.img}')
            delete_photo.delete()
    return render(request, 'photos.html', data)


@login_required(login_url='home')
def music(request):
    userid = getAuthUser(request)
    personal_data = getUser(userid)
    form = UserMusicForm()
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    allSong = UserMusic.objects.all()

    data = {
        'userid': userid,
        'allDialogues': allDialogues,
        'unread_messages': unread_messages,
        'allSong': allSong,
        'form': form,
        'personal_data': personal_data
    }

    if request.method == "POST":
        form = UserMusicForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = userid
            if form.title == '':
                form.title = str(form.song)[:-4]
            form.save()
    return render(request, 'music.html', data)


def loginOut(request):
    logout(request)
    return redirect('/')


def forgot(request):
    return render(request, 'forgot.html')


@login_required(login_url='home')
def main(request, pk):
    clean_id = re.findall(r'\d+', request.path)
    form = UserWallForm()
    userid = getAuthUser(request)
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    personal_data = getUser(userid)

    friends = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.to_user = up.user_id WHERE fl.from_user = {userid} and fl.friends = 1')

    followers = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {userid} and fl.friends = 0')
    userPhoto = UserPhotos.objects.filter(user_id=userid).order_by('-time_create')[:7]
    posts = UserWall.objects.raw(
        f'SELECT * FROM MYSITE_USERWALL UW JOIN MYSITE_USERPROFILE UP ON UW.USER_SENDER_ID = UP.USER_ID WHERE UW.USER_RECIPIENT_ID = {userid} ORDER BY UW.TIME_CREATE DESC')
    
    like_list = UserWall.objects.raw(f'SELECT * FROM MYSITE_USERWALL_LIKES UWL JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = UWL.USER_ID')
    dislike_list = UserWall.objects.raw(f'SELECT * FROM MYSITE_USERWALL_DISLIKES UWD JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = UWD.USER_ID')
    req_user = request.user
    data = {
        'form': form,
        'friends': friends,
        'followers': followers,
        'allDialogues': allDialogues,
        'unread_messages': unread_messages,
        'len_followers': len(followers),
        'userid': userid,
        'personal_data': personal_data,
        'userPhoto': userPhoto,
        'posts': posts,
        'req_user': req_user,
        'like_list': like_list,
        'dislike_list' : dislike_list,
    }

    if int(clean_id[0]) != userid:
        return redirect(f'/id{userid}')
    else:
        if request.method == "POST":
            form = UserWallForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_sender_id = userid
                form.user_recipient_id = userid
                if form.img:
                    UserPhotos.objects.create(content=form.content, img=form.img, user_id=userid)
                form.save()
            else:
                post_form = request.POST
                try:
                    post = UserWall.objects.get(id=post_form['post_id_like'])
                    if not request.user in post.likes.all():
                        if not request.user in post.dislikes.all():
                            post.likes.add(request.user)
                        else:
                            post.dislikes.remove(request.user)
                            post.likes.add(request.user)
                    else:
                        post.likes.remove(request.user)
                except:
                    try:
                        post = UserWall.objects.get(id=post_form['post_id_dislike'])
                        if not request.user in post.dislikes.all():
                            if not request.user in post.likes.all():
                                post.dislikes.add(request.user)
                            else:
                                post.likes.remove(request.user)
                                post.dislikes.add(request.user)
                        else:
                            post.dislikes.remove(request.user)
                    except:
                        try:
                            post = UserWall.objects.get(id=post_form['post_id'])
                            try:
                                os.remove(f'{CURR_DIR}{post.img}')
                                UserPhotos.objects.get(img=post.img).delete()
                                post.delete()
                            except:
                                try:
                                    UserPhotos.objects.get(img=post.img).delete()
                                    post.delete()
                                except:
                                    post.delete()
                        except:
                            pass
        return render(request, 'main.html', data)


@login_required(login_url='home')
def viewUser(request, pk):
    clean_id = re.findall(r'\d+', request.path)  # Получение id пользователя
    userid = getAuthUser(request)  # Получение личного id
    personal_data = getUser(userid)
    allDialogues = getAllMessages(userid)
    unread_messages = calculation_unread(allDialogues, userid)
    req_user = request.user
    user_followers = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {userid} and fl.friends = 0')

    if int(clean_id[0]) == userid or int(clean_id[0]) == 1:
        return redirect(f'/id{userid}')
    else:
        form = UserWallForm()
        delete_friend_form = DeleteFriendForm(initial={'from_user': userid, 'to_user': clean_id[0]})
        photos = UserPhotos.objects.filter(user_id=clean_id[0])[:7]
        music = UserMusic.objects.filter(user_id=clean_id[0])
        posts = posts = UserWall.objects.raw(
            f'SELECT * FROM MYSITE_USERWALL UW JOIN MYSITE_USERPROFILE UP ON UW.USER_SENDER_ID = UP.USER_ID WHERE UW.USER_RECIPIENT_ID = {clean_id[0]} ORDER BY UW.TIME_CREATE DESC')
        friends = FriendsList.objects.raw(
            f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {clean_id[0]} and fl.friends = 1')
        followers = FriendsList.objects.raw(
            f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {clean_id[0]} and fl.friends = 0')
        user_profile = UserProfile.objects.get(user_id=clean_id[0])
        check_from = FriendsList.objects.filter(from_user=userid, to_user=clean_id[0])
        check_to = FriendsList.objects.filter(from_user=clean_id[0], to_user=userid)
        like_list = UserWall.objects.raw(f'SELECT * FROM MYSITE_USERWALL_LIKES UWL JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = UWL.USER_ID')
        dislike_list = UserWall.objects.raw(f'SELECT * FROM MYSITE_USERWALL_DISLIKES UWD JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = UWD.USER_ID')

        data = {
            'len_followers': len(user_followers),
            'check_from': check_from,
            'check_to': check_to,
            'followers': followers,
            'userid': userid,
            'allDialogues': allDialogues,
            'unread_messages': unread_messages,
            'form': form,
            'delete_friend_form': delete_friend_form,
            'clean_id': clean_id[0],
            'photos': photos,
            'music': music,
            'posts': posts,
            'friends': friends,
            'user_profile': user_profile,
            'personal_data': personal_data,
            'req_user': req_user,
            'like_list': like_list,
            'dislike_list': dislike_list,
        }

        if request.method == "POST":
            post_form = request.POST
            leave_note = UserWallForm(request.POST, request.FILES)
            if leave_note.is_valid():
                leave_note = leave_note.save(commit=False)
                leave_note.user_sender_id = userid
                leave_note.user_recipient_id = clean_id[0]
                leave_note.save()
            else:
                post_form = request.POST
                try:
                    post = UserWall.objects.get(id=post_form['post_id_like'])
                    if not request.user in post.likes.all():
                        if not request.user in post.dislikes.all():
                            post.likes.add(request.user)
                        else:
                            post.dislikes.remove(request.user)
                            post.likes.add(request.user)
                    else:
                        post.likes.remove(request.user)
                except:
                    try:
                        post = UserWall.objects.get(id=post_form['post_id_dislike'])
                        if not request.user in post.dislikes.all():
                            if not request.user in post.likes.all():
                                post.dislikes.add(request.user)
                            else:
                                post.likes.remove(request.user)
                                post.dislikes.add(request.user)
                        else:
                            post.dislikes.remove(request.user)
                    except:
                        try:
                            post = UserWall.objects.get(id=post_form['post_id'])
                            try:
                                os.remove(f'{CURR_DIR}{post.img}')
                                UserPhotos.objects.get(img=post.img).delete()
                                post.delete()
                            except:
                                try:
                                    UserPhotos.objects.get(img=post.img).delete()
                                    post.delete()
                                except:
                                    post.delete()
                        except:
                            try:
                                post = request.POST
                                if post['from_user']:                           
                                    if not check_from and not check_to:
                                        FriendsList.objects.create(from_user=post['from_user'], to_user=post['to_user'])
                                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                                    elif not check_from and check_to:
                                        FriendsList.objects.create(from_user=post['from_user'], to_user=post['to_user'],
                                                                friends=1)
                                        FriendsList.objects.filter(from_user=post['to_user'], to_user=post['from_user']).update(
                                            friends=1)
                                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                                    else:
                                        FriendsList.objects.filter(from_user=userid,
                                                                to_user=clean_id[0]).delete()
                                        FriendsList.objects.filter(from_user=clean_id[0], to_user=userid).update(
                                            friends=0)
                                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                            except:
                                pass                                
        return render(request, 'view_user.html', data)

class ValidateData(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        context = {
            'has_username': User.objects.filter(username__iexact=username).exists(),
            'has_email': UserProfile.objects.filter(email__iexact=email).exists(),
        }
        return JsonResponse(context)