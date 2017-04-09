#-*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.conf import settings
import random
import time
import smtplib
from django.utils import timezone

import hashlib
from django.conf import settings
from django.core.mail import send_mail

def html_mail(subject, message, receiver):
    """Send email with default SMTP server"""
    _email = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=list(receiver),fail_silently=False )
    return _email

def gen_random_url_short():
    """Random URL generator short version"""
    pool = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"""
    random_pool = ''
    for i in range(0, 32):
        random_pool = random_pool + random.choice(pool)
    return random_pool


def gen_random_url():
    """Random URL generator, crypto valid"""
    pool = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"""
    random_pool = ''
    for i in range(0, 164):
        random_pool = random_pool + random.choice(pool)
    time.sleep(random.random())
    url_part, get_param = random_pool[:128], random_pool[128:]
    complete_url = url_part + '-' + get_param
    return complete_url


def gen_random_pass():
    pool = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"""
    random_pass = ''
    for i in range(0, 6):
        random_pass = random_pass + random.choice(pool[:25])

    return random_pass


class Keys(models.Model):
    user = models.ForeignKey(User, verbose_name="Utilisateur")
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name="Date de publication")
    content = models.TextField(max_length=950, verbose_name="Clef")
    key_type = models.CharField(max_length=32, verbose_name="Type de clef")
    name = models.CharField(max_length=18)

    def __unicode__(self):
        return '{}'.format(str(self.id))


@receiver(post_delete, sender=Keys)
def decrement_profil_key_nb(sender, instance, using, **kwargs):
    if instance:
        profil = Profil.objects.get(user=instance.user)
        profil.key_nb = profil.key_nb - 1
        profil.save()



def default_date():
    return timedelta(30, 0, 0) + timezone.now()

class InvitationUrls(models.Model):
    url_uuid = models.CharField(max_length=175, default=gen_random_url_short)
    name = models.CharField(max_length=32,
                            verbose_name="Utilisateur")
    email = models.EmailField(unique=False)
    date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(auto_now_add=False,
                                           verbose_name="Expire",
                                           default=default_date)
    tried = models.IntegerField(default=0)
    active = models.BooleanField(verbose_name="Activée", default=True)
    message = models.CharField(max_length=175)
    #-UserInvitations
    sender_user=models.ForeignKey(User, verbose_name="Utilisateur", unique=False)

    def __unicode__(self):
        return '{}, {}'.format(self.name, self.email)


@receiver(post_save, sender=InvitationUrls)
def email_sender_after_create_invitation(sender, instance, using, raw, created,
                                         **kwargs):
    if created:
        text = """ Bonjour {}, vous êtes invité à rejoindre le résau smalakey,\n
        Ce réseau permet l'échange de clef publiques rétroshare avec notre communauté. Attention, le site n'est accessible que sur invitation, inscrivez vous avec le lien ci dessous lors de votre première visite.
        http://www.{}/{}-/
         </br> \n""".format(
            instance.name,
            settings.DOMAIN_URL + '/exchange/sign_up',
            instance.url_uuid )
        html_mail("Invitation de " +instance.sender_user.username+" pour Smalakey", text, [instance.email])



class Profil(models.Model):
    user = models.OneToOneField(User)  # La liaison OneToOne vers le modèle User
    spec_url = models.ForeignKey(InvitationUrls)
    key_nb = models.IntegerField(default=0)


class PasswordResetUrl(models.Model):
    url_uuid = models.CharField(max_length=175, default=gen_random_url_short)
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(auto_now_add=False,
                                           verbose_name="Expire",
                                           default=default_date)
    tried = models.IntegerField(default=0)
    active = models.BooleanField(verbose_name="Activée", default=True)

    def __unicode__(self):
        return '{}'.format(self.email)



@receiver(post_save, sender=PasswordResetUrl)
def email_sender_after_create_password_reset_url(sender, instance, using, raw,
                                                 created, **kwargs):

    if created:
        text = """ Bonjour , voici votre lien de reinitalisation de mot de passe.
        http://www.{}/{}-/
         </br> \n""".format(
            settings.DOMAIN_URL + '/exchange/sign_up',
            instance.url_uuid )
        html_mail("Reset du mot de passe", text, [instance.email])


class FriendsRequests(models.Model):
    sender_user = models.ForeignKey(
        User,
        related_name='friends_requests_sender_user')
    receiver_user = models.ForeignKey(
        User,
        related_name='friends_requests_receiver_user')
    message = models.CharField(max_length=150, default=gen_random_url_short)
    read=  models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
