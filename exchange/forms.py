#-*- coding: utf-8 -*-
import re
import hashlib
from django import forms
from exchange.models import InvitationUrls, Keys, Profil, PasswordResetUrl, FriendsRequests
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import base64
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm

class SignUpForm(forms.Form):
    """ Fomulaire d'invitation, il ne doit etre initialisé et nettoyé qu'une seule fois dans la vue"""


    username = forms.CharField(min_length=4, label="Pseudo")
    email = forms.EmailField(
        max_length=30,
        label="L'email qui a été utilisé pour vous inviter.")
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(),
                               label="Mot de passe")
    password_ = forms.CharField(min_length=6,
                                widget=forms.PasswordInput(),
                                label="Retaper mot de passe")

    def __init__(self, *args, **kwargs):
        self.invitation = kwargs.pop('invitation', None)
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_')
        if pass1 != pass2:
            raise forms.ValidationError(
                "Les mots de passe ne correpondent pas.")
        if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', pass1):
            pass
        elif len(pass1)==6 :
            raise forms.ValidationError("Utilisez au moins un chiffre et une lettre dans votre mot de passe, car seulement 6 caractères, c'est court...")
        if cleaned_data.get('email') != self.invitation.email:
            self.invitation.tried = int(self.invitation.tried) + 1
            if 6 - self.invitation.tried < 0:
                self.invitation.active = False
                self.invitation.save()
                raise forms.ValidationError(
                    "Vous avez épuisé vos tentatives, contactez l'administrateur. Bisoux")
            self.invitation.save()
            raise forms.ValidationError(
                "L'email que vous avez fourni n'est pas le bon. Attention, il vous reste {} tentatives.".format(
                    6 - self.invitation.tried))
        if User.objects.filter(
                username=self.cleaned_data.get("username")).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, label="Pseudo")
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(),
                               label="Mot de passe")


class ResetForm(forms.Form):
    email = forms.EmailField(max_length=30, error_messages='')

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)

        except:
            raise forms.ValidationError(
                "Il est possible que nous vous ayons déjà envoyé un email de reinitialisation depuis moins d'une semaine ou que ce compte n'existe pas, contactez l'administrateur")
            return cleaned_data

        reset = PasswordResetUrl.objects.filter(email=user.email)
        date_constraint = True
        if len(reset) != 0:
            last_reset = reset.order_by('-date')[0]
            if (last_reset.date + timedelta(7, 0, 0) > timezone.now()):
                date_constraint = False
        if not date_constraint or not user:
            raise forms.ValidationError(
                "Il est possible que nous vous ayons déjà envoyé un email de reinitialisation depuis moins d'une semaine ou que ce ceompte n'existe pas, contactez l'administrateur")

        return cleaned_data


class PasswordResetForm(forms.Form):
    """ Fomulaire d'password_url, il ne doit etre initialisé et nettoyé qu'une seule fois dans la vue"""
    email = forms.EmailField(
        max_length=30,
        label="L'email qui a été utilisé pour vous inviter.")
    new_password = forms.CharField(min_length=6,
                                   widget=forms.PasswordInput(),
                                   label="Mot de passe")
    password_ = forms.CharField(min_length=6,
                                widget=forms.PasswordInput(),
                                label="Retaper mot de passe")

    def __init__(self, *args, **kwargs):
        self.password_url = kwargs.pop('password_url', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        pass1 = cleaned_data.get('new_password')
        pass2 = cleaned_data.get('password_')
        if pass1 != pass2:
            raise forms.ValidationError(
                "Les mots de passes ne correpondent pas.")

        if cleaned_data.get('email') != self.password_url.email:
            self.password_url.tried = int(self.password_url.tried) + 1
            if 4 - self.password_url.tried < 0:
                self.password_url.active = False
                self.password_url.save()
                raise forms.ValidationError(
                    "Vous avez épuisé vos tentatives, contactez l'administrateur. Bisoux")
            self.password_url.save()
            raise forms.ValidationError(
                "L'email que vous avez fourni n'est pas le bon. Attention, il ne vous reste que {} tentatives , c'est craignos.".format(
                    4 - self.password_url.tried))

        return cleaned_data


class ChangePassForm(forms.Form):
    user_password = forms.CharField(min_length=6,
                                    widget=forms.PasswordInput(),
                                    label="Votre mot de passe actuel")
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(),
                               label="Nouveau mot de passe")
    password_ = forms.CharField(widget=forms.PasswordInput(),
                                label="Retaper nouveau mot de passe")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePassForm, self).__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super(ChangePassForm, self).clean()
        old_password = cleaned_data.get('user_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "Votre mot de passe actuel n'est pas bon.")
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_')
        if pass1 != pass2:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas.")

        return cleaned_data


CHOICES = (("Retroshare", "Retroshare"), )


class SubmitKey(forms.Form):
    """ Attention au nettoyagfe du formulaire, le nom de la clef ne doit etre verifié que pour l'utilisateur courant. Passer l'id de l'utilisateur à l'initialisation de l'instance Submit"""
    clef = forms.CharField(widget=forms.Textarea)
    type_de_clef = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    nom = forms.CharField(min_length=4, max_length=18)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SubmitKey, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SubmitKey, self).clean()
        nom = cleaned_data.get('nom')

#-UserInvitations

        # ATTENTION: la recherche de la clef doit se faire pur l'utilisateur couurant et non pour TOUS els utilsiateurs mother fucker bitch.


        if Keys.objects.filter(name=nom, user=self.user).exists():
            raise forms.ValidationError(
                "Vous avez déjà utilisé ce nom de clef. ")
        try:
            clef = cleaned_data.get('clef')
            decoded_key = base64.standard_b64decode(clef)
        except:
            raise forms.ValidationError("Votre clef n'est pas valide.")
        if "(Generated by RetroShare)" not in decoded_key:
            raise forms.ValidationError(
                "Cette clef ne semble pas être une clef Rétroshare. Peut être n'utilisez vous pas une bonne version.")
        return cleaned_data


class DeleteKey(forms.Form):
    key_to_delete = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DeleteKey, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(DeleteKey, self).clean()
        key_id = cleaned_data.get('key_to_delete')
        try:
            the_key = Keys.objects.get(id=key_id)
        except:
            raise forms.ValidationError(
                "Cette clef n'existe pas, t'essaierais pas de me gruger ?")
        list_user_key = Keys.objects.filter(
            user__username=self.request.user.username)
        if the_key not in list_user_key:

            raise forms.ValidationError(
                "Cette clef ne t'appartient pas petit canaillou !")

        return cleaned_data


CHOICES = (('Oui', 'Oui', ), ('Non', 'Non', ))

#Mangeur de viande histoire de mammouth marylene patoumatis.

class FriendRequestForm(forms.Form):

    message = forms.CharField(
        widget=forms.Textarea,
        max_length=149,
        label=
        "Ajouter un message pour qu'il sache qui vous êtes et ce que vous voulez partager.")

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.receiver = kwargs.pop('receiver', None)
        super(FriendRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(FriendRequestForm, self).clean()

        if len(FriendsRequests.objects.filter(sender_user=self.sender,
                                            receiver_user=self.receiver))>0:
            raise forms.ValidationError("Vous avez déjà envoyé une requête à cet utilisateur.")
        if self.sender==self.receiver:
            raise forms.ValidationError("Vous ne pouvez pas vous envoyer une invitation à vous même , bouffon.")
        return cleaned_data


class InvitationForm(forms.Form):

    email=forms.EmailField(max_length=30,label="L'email de la personne que vous voulez inviter.")
    name=forms.CharField(min_length=4, label="Pseudo")
    message=forms.CharField(max_length=175, label="Message",widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(InvitationForm, self).clean()
        email = cleaned_data.get('email')
        user_obj=User.objects.get(pk=self.user)
        if InvitationUrls.objects.filter(email=email).count() > 0 and user_obj.is_superuser==False :
            raise forms.ValidationError("Cet utilisateur à déjà recu une invitation, Demandez lui son pseudo sur le site :) .")
        try:
            user_invitations=InvitationUrls.objects.filter(sender_user=self.user).count()
        except:
            raise forms.ValidationError("Vous n'êtes pas identifié, identifiez vous ou passez votre chemin.")
        if user_invitations >=7 and user_obj.is_superuser==False :
            raise forms.ValidationError(" Vous avez déjà posté sept ivitations, contactez l'administrateur")
        return cleaned_data


