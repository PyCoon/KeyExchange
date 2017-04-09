#-*- coding: utf-8 -*-
import re
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.static import serve
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from exchange.forms import SignUpForm, LoginForm, ResetForm, PasswordResetForm, SubmitKey, ChangePassForm, DeleteKey, FriendRequestForm, InvitationForm
from exchange.models import InvitationUrls, Keys, Profil, PasswordResetUrl, FriendsRequests
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail

def html_mail(subject, message, receiver):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=list(receiver),fail_silently=False )
@login_required
def front_page(request):
    """ Page d'acceuil.  """


    return render(request, 'front_page.tpl', locals())


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/message.tpl',
                  {'message': "Vous avez été déconnecté"})


@login_required
def change_pass_view(request):
    """ Url de changement de mot de passe """
    if request.method == "POST":
        form = ChangePassForm(request.POST, user=request.user)
        if form.is_valid():

            user = User.objects.get(username=request.user.username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            message = {'message':
                       "Votre changement de mot de passe a été pris en compte"}

            return render(request, 'registration/message.tpl', locals())
        return render(request, 'registration/change_pass.tpl', locals())
    else:
        form = ChangePassForm(user=request.user)
        return render(request, 'registration/change_pass.tpl', locals())


@login_required
def account_detail(request):
    """Page de gestiond e l'utilisateur. Permet de supprimer les clefs."""

    if request.method == "POST":
        # Delete form gen
        form_ = DeleteKey(request.POST, request=request)  # ICI
        if form_.is_valid():
            deleted_key_id = form_.cleaned_data['key_to_delete']
            to_deleted = Keys.objects.get(id=deleted_key_id)
            # Javascript message on template
            message = u"La clef {} a été supprimée.".format(to_deleted.name)
            to_deleted.delete()
            keys = Keys.objects.filter(user__id=request.user.id)
            forms_and_keys = []
            for key in keys:
                forms_and_keys.append([key, DeleteKey(initial={'key_to_delete':
                                                               key.id},
                                                      request=request)])
    else:
        keys = Keys.objects.filter(user__id=request.user.id)
        friend_requests_list = FriendsRequests.objects.filter(
            receiver_user=request.user)
        paginator = Paginator(friend_requests_list, 10)
        page = request.GET.get('page')
        try:
            friend_requests = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            friend_requests = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            friend_requests = paginator.page(paginator.num_pages)
        forms_and_keys = []
        for key in keys:
            forms_and_keys.append([key,
                                   DeleteKey(initial={'key_to_delete': key.id},
                                             request=request)])  # ICI

    return render(request, 'registration/account.tpl', locals())

@login_required
def note_notif_as_read(request):
    """ Efface les notifications de l'utilisateurs sur sa page d'acceuil (FriendRequest)  """
    notifs = FriendsRequests.objects.filter(receiver_user=request.user, read=False )
    read_ = []
    for notif in notifs:
        notif.read =True
        read_.append(notif)
    saved_ = [ readed.save() for readed in read_ ]
    request.session['notifications'] = 0
    return redirect(account_detail)

def sign_up(request, invitation_url):  # En chantier  bébé
    """ Enregistrement d'un utilisateur après reception d'une InvitationUrl """
    invitation = get_object_or_404(InvitationUrls, url_uuid=invitation_url)
    if invitation.active and invitation.expiration_date > timezone.now():
        if request.method == "POST":
            form = SignUpForm(request.POST, invitation=invitation)

            if form.is_valid():
                try:
                    user = User.objects.create_user(form.cleaned_data["username"],
                                                invitation.email,
                                                form.cleaned_data["password"])
                    profil = Profil(user=user,
                                    spec_url=invitation)
                    user.save()
                    profil.save()
                    invitation.active = False
                    invitation.save()
                except:
                    # If error delete user instance on database.
                    user.delete()
                    profil.delete()
                    invitation.active = False
                    invitation.save()
                    return HttpResponse("Une erreur est survenue, votre invitation a été supprimée, l'administrateur à été prévenu.")




                return render(request, 'registration/message.tpl',
                              {'message':
                               'Votre compte a été enregistré {}'.format(
                                   form.cleaned_data["username"])})
            else:
                return render(request, 'registration/sign_up.tpl', locals())
        else:

            form = SignUpForm()
            return render(request, 'registration/sign_up.tpl', locals())
    else:
        return HttpResponse('404')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Initialisation du compteur de notifications.
                    request.session['notifications']=FriendsRequests.objects.filter(receiver_user=user, read=False ).count()
                    return redirect(front_page)
        message = u"La combinaison mot nom d'utilisateru, mot de passe est invalide."
        return render(request, 'registration/login.tpl', locals())
    else:
        form = LoginForm()
        return render(request, 'registration/login.tpl', locals())


def password_reset(request):
    """ For reset pass, use receiver on model for send email to user """
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            if user.is_active:
                url_pass = PasswordResetUrl(email=user.email)
                url_pass.save()
                return HttpResponse("Merci, un email vous as été envoyé.")
        else:
            form = ResetForm(request.POST)
            return render(request, 'registration/password_reset_form.tpl',
                          locals())

    else:
        form = ResetForm()
        return render(request, 'registration/password_reset_form.tpl',
                      locals())


def do_reset_password_now(request, reset_url):
    """ Reset du password, utilise un mail.  """

    password_url = get_object_or_404(PasswordResetUrl, url_uuid=reset_url)
    if password_url.active and password_url.expiration_date > timezone.now():
        if request.method == "POST":
            form = PasswordResetForm(request.POST, password_url=password_url)

            if form.is_valid():
                user = User.objects.get(
                    email__exact=form.cleaned_data['email'])
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                password_url.active = False
                password_url.save()
                return render(request, 'registration/message.tpl',
                              {'message':
                               'Votre mot de passe a été reinitialisé. {}'})
            else:
                return render(request,
                              'registration/password_reset_confirm.tpl',
                              locals())
        else:

            form = PasswordResetForm()
            return render(request, 'registration/password_reset_confirm.tpl',
                          locals())
    else:
        return HttpResponse('404')


@login_required
def upload_key(request):
    """ Envoi d'une clef sur le serveur """
    if request.method == "POST":
        form = SubmitKey(request.POST, user=request.user)

        if form.is_valid():

            user_ = request.user
            if len(Keys.objects.filter(content=form.cleaned_data[
                    "clef"])) != 0:
                return HttpResponse(content='Déolé, cette clef existe déja.')
            elif int(user_.profil.key_nb) >= 5:
                return HttpResponse(
                    content=
                    'Vous avez déjà plus de 5 clefs actives. Sont-elle vraiment toutes actives ?')
            key = Keys(user=request.user,
                       key_type=form.cleaned_data["type_de_clef"],
                       content=form.cleaned_data["clef"],
                       name=form.cleaned_data["nom"])
            key.save()
            user_.profil.key_nb = 1 + user_.profil.key_nb
            user_.profil.save()

            return redirect(account_detail)

    else:
        form = SubmitKey(initial={"nom": "Clef n°{}".format(str(
            request.user.profil.key_nb + 1))}, user=request.user)
    return render(request, 'upload_key.tpl', locals())


class AllUserList( ListView):


    model = User
    context_object_name = "users"
    template_name = "display_all_users.tpl"
    paginate_by = 50


    def get_queryset(self):
        self.users = User.objects.order_by('-date_joined')
        return self.users


def user_detail(request, pk):
    """ Voir le detail d'un utilsiateur """
    user = User.objects.get(id=pk)
    keys = Keys.objects.filter(user=user)
    if request.method == "POST" and len(keys) > 0:
        form = FriendRequestForm(request.POST,
                                 sender=request.user.id,
                                 receiver=pk)
        if form.is_valid():
            friend_request = FriendsRequests.objects.create(
                sender_user=request.user,
                receiver_user=user,
                message=form.cleaned_data['message'])
            friend_request.save()
            sended=True
            return render(request, 'other_user_detail.tpl', locals())
    else:
        if len(keys) > 0:
            form = FriendRequestForm(sender=request.user.id, receiver=pk)
    return render(request, 'other_user_detail.tpl', locals())


class LastUsersKeyPosted(ListView):

    model = Keys
    context_object_name = "last_users_keys"
    template_name = "display_last_users_keys.tpl"
    paginate_by = 30

    @login_required
    def get_queryset(self):
        self.users_keys = Keys.objects.order_by('-date')
        return self.users_keys


@login_required
def create_invitation(request):
    if request.method=="POST":
        form=InvitationForm(request.POST, user=request.user.pk)
        if form.is_valid():
            invitation=InvitationUrls(sender_user=request.user)
            invitation.email=form.cleaned_data["email"]
            invitation.message=form.cleaned_data["message"]
            invitation.save()

            name=form.cleaned_data["name"]

    else:
        form=InvitationForm( user=request.user)
    return render(request, 'invitation_send.tpl', locals())
