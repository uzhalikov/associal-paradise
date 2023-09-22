from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from datetime import datetime
import re


def getAuthUser(request):
    return request.session.get('is_auth', False)


class AllUsers(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'users.html'
    context_object_name = 'AllUsers'
    login_url = 'home'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userid'] = self.request.session.get('is_auth', False)
        context['personal_data'] = UserProfile.objects.get(id=context['userid'])
        return context

    def get_queryset(self):
        userid = self.request.session.get('is_auth', False)
        data = UserProfile.objects.exclude(user_id=userid) & UserProfile.objects.exclude(
            user_id=1)  # Ислючение двух пользователей
        return data


class UpdateUser(UpdateView):
    model = UserProfile
    template_name = 'change.html'
    form_class = UserProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userid'] = self.request.session.get('is_auth', False)
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
    userid = getAuthUser(request)
    if userid != False:
        return redirect(f'/id{userid}')
    else:
        if request.method == 'POST':
            data = request.POST
            User.objects.create_user(username=data['username'], email=data['email'], password=data['password'],
                                     first_name=data['first_name'], last_name=data['last_name'])
            new_user_id = User.objects.get(username=data['username'])
            UserProfile.objects.create(user_id=new_user_id.id, first_name=new_user_id.first_name,
                                       last_name=new_user_id.last_name, email=new_user_id.email)
            congr = 'Поздравляем! Вы успешно зарегистрировались и можете авторизоваться в системе.'
        return render(request, 'reg.html', {'congr': congr})


def getUser(userid):
    return UserProfile.objects.get(user_id=userid)


@login_required(login_url='home')
def dialogues(request):
    userid = getAuthUser(request)
    personal_data = UserProfile.objects.get(id=userid)
    allDialogues = HaveDialog.objects.raw(
        f'select 1 as id, up.first_name as name_sender, up2.first_name as name_recipient, hd.user_recipient_id, hd.user_sender_id, hd.status_message, up.avatar, hd.last_message from mysite_havedialog hd join mysite_userprofile up on up.user_id = hd.user_sender_id join mysite_userprofile up2 on up2.user_id = hd.user_recipient_id where hd.user_recipient_id = {userid}')
    data = {
        'userid': userid,
        'allDialogues': allDialogues,
        'personal_data': personal_data
    }
    return render(request, 'dialogues.html', data)


@login_required(login_url='home')
def viewDialogues(request, pk):
    clean_id = re.findall(r'\d+', request.path)  # Получение id пользователя
    userid = getAuthUser(request)
    personal_data = UserProfile.objects.get(id=userid)
    form = DialogsForm()
    dialogues = Dialogs.objects.raw(
        f'select * from mysite_dialogs di join mysite_userprofile up on di.user_sender_id = up.user_id where di.user_sender_id = {clean_id[0]} and di.user_recipient_id = {userid} or di.user_sender_id = {userid} and di.user_recipient_id = {clean_id[0]} order by di.time_create desc')
    user_info = UserProfile.objects.raw(
        f'select * from mysite_userprofile up join auth_user au on au.id = up.user_id where up.user_id = {clean_id[0]}')
    try:
        dialogObj = HaveDialog.objects.get(user_sender_id=clean_id[0], user_recipient_id=userid)
        dialogObj.status_message = 1
        dialogObj.save()
    except:
        pass

    data = {
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
                                          last_message=form.private_message)
                HaveDialog.objects.create(user_sender_id=clean_id[0], user_recipient_id=userid,
                                          last_message=form.private_message)
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
                secObj.status_message = False
                firstObj.save()
                secObj.save()
            form.save()
    return render(request, 'viewDialogues.html', data)


@login_required(login_url='home')
def viewChat(request):
    userid = getAuthUser(request)
    personal_data = UserProfile.objects.get(id=userid)
    form = ChatForm()
    allMessages = AllChat.objects.raw(
        'SELECT * FROM MYSITE_ALLCHAT CH JOIN MYSITE_USERPROFILE UP ON UP.USER_ID = CH.USER_ID ORDER BY CH.MSG_TIME_CREATE DESC')

    data = {
        'userid': userid,
        'form': form,
        'allMessages': allMessages,
        'personal_data': personal_data
    }

    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = userid
            form.save()
    return render(request, 'chat.html', data)


@login_required(login_url='home')
def photos(request):
    userid = getAuthUser(request)
    personal_data = UserProfile.objects.get(id=userid)
    userPhoto = UserPhotos.objects.filter(user_id=userid).order_by('-time_create')
    form = UserPhotosForm()
    data = {
        'userid': userid,
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
    return render(request, 'photos.html', data)


@login_required(login_url='home')
def music(request):
    userid = getAuthUser(request)
    personal_data = UserProfile.objects.get(id=userid)
    form = UserMusicForm()
    allSong = UserMusic.objects.all()

    data = {
        'userid': userid,
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
    personal_data = UserProfile.objects.get(id=userid)
    friends = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.to_user = up.user_id WHERE fl.from_user = {userid} and fl.friends = 1')


    followers = FriendsList.objects.raw(
        f'SELECT * FROM MYSITE_friendslist fl JOIN MYSITE_userprofile up on fl.from_user = up.user_id WHERE fl.to_user = {userid} and fl.friends = 0')
    user = User.objects.get(id=userid)
    userPhoto = UserPhotos.objects.filter(user_id=userid).order_by('-time_create')[:7]
    posts = UserWall.objects.raw(
        f'SELECT * FROM MYSITE_USERWALL UW JOIN MYSITE_USERPROFILE UP ON UW.USER_SENDER_ID = UP.USER_ID WHERE UW.USER_RECIPIENT_ID = {userid} ORDER BY UW.TIME_CREATE DESC')

    data = {
        'form': form,
        'friends': friends,
        'followers': followers,
        'len_followers': len(followers),
        'userid': userid,
        'personal_data': personal_data,
        'user': user,
        'userPhoto': userPhoto,
        'posts': posts,
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
        return render(request, 'main.html', data)


@login_required(login_url='home')
def viewUser(request, pk):
    clean_id = re.findall(r'\d+', request.path)  # Получение id пользователя
    userid = getAuthUser(request)  # Получение личного id
    personal_data = UserProfile.objects.get(id=userid)
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

        data = {
            'len_followers': len(user_followers),
            'check_from': check_from,
            'check_to': check_to,
            'followers': followers,
            'userid': userid,
            'form': form,
            'delete_friend_form': delete_friend_form,
            'clean_id': clean_id[0],
            'photos': photos,
            'music': music,
            'posts': posts,
            'friends': friends,
            'user_profile': user_profile,
            'personal_data': personal_data,
        }

        if request.method == "POST":
            add_friend = request.POST
            delete_friend = DeleteFriendForm(request.POST)
            leave_note = UserWallForm(request.POST, request.FILES)
            if leave_note.is_valid():
                leave_note = leave_note.save(commit=False)
                leave_note.user_sender_id = userid
                leave_note.user_recipient_id = clean_id[0]
                leave_note.save()
            else:
                if not check_from and not check_to:
                    FriendsList.objects.create(from_user=add_friend['from_user'], to_user=add_friend['to_user'])
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                elif not check_from and check_to:
                    FriendsList.objects.create(from_user=add_friend['from_user'], to_user=add_friend['to_user'],
                                               friends=1)
                    FriendsList.objects.filter(from_user=add_friend['to_user'], to_user=add_friend['from_user']).update(
                        friends=1)
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                else:
                    #FriendsList.objects.filter(from_user=delete_friend['from_user'].value(), to_user=delete_friend['to_user'].value(), friends=1).delete()
                    #FriendsList.objects.filter(from_user=delete_friend['to_user'].value(), to_user=delete_friend['from_user'].value(), friends=1).delete()
                    FriendsList.objects.filter(from_user=userid,
                                               to_user=clean_id[0]).delete()
                    FriendsList.objects.filter(from_user=clean_id[0], to_user=userid).update(
                        friends=0)
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return render(request, 'view_user.html', data)
