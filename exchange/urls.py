#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from exchange.views import LastUsersKeyPosted, AllUserList


admin.autodiscover()

urlpatterns = patterns('exchange.views',
    # User manipulation
    url(r"^sign_up/(?P<invitation_url>[0-9a-zA-Z\_]{32})[\-]{1}/$", 'sign_up', name="sign_up"),
    url(r'^login/$', 'login_user', name="login_user" ),
    url(r'^password_reset/$', 'password_reset', name="password_reset" ),
    url(r"^do_reset_password_now/(?P<reset_url>[0-9a-zA-Z\_]{32})[\-]{1}/$", 'do_reset_password_now', name="do_reset_password_now"),
    url(r"^logout/$", 'logout_view', name="logout_view"),
    url(r"^change_pass/$", 'change_pass_view', name="change_pass_view"),
    url(r"^account/$", 'account_detail', name="account_detail"),

    # Tutorials
    url(r'^tutoriels/$', login_required(TemplateView.as_view(template_name="tutoriels/tutoriels.tpl")), name="tutoriels" ),
    url(r'^tutoriels/ajouter_ami/$',  login_required(TemplateView.as_view(template_name="tutoriels/ajouter_ami.tpl")), name="ajouter_ami" ),
    url(r'^tutoriels/installation/$', login_required(TemplateView.as_view(template_name="tutoriels/installation.tpl")), name="installation" ),
    url(r'^tutoriels/partager/$', login_required(TemplateView.as_view(template_name="tutoriels/partager.tpl")), name="partager" ),

    # Site content
    url(r'^upload_key/$', 'upload_key', name='upload_key'),
    url(r'^$', 'front_page', name='front_page'),

    # Display user content
     url(r'^last_users_keys/$', login_required(LastUsersKeyPosted.as_view()) , name="last_users_keys"),  # Via la fonction as_view, comme vu tout à l'heure
     url(r'^all_users_list/$',login_required( AllUserList.as_view()), name="all_users_list"),
     url(r'^detail_user_key/(?P<pk>\d+)$','user_detail', name="detail_user_key"),
     
     url(r'^create_invitation/$','create_invitation', name="create_invitation"),

     
url(r'^note_notif_as_read/$','note_notif_as_read', name="note_notif_as_read"),

                       )
