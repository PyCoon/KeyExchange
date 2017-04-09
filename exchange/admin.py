#-*- coding: utf-8 -*-

from django.contrib import admin
from exchange.models import Keys, InvitationUrls, Profil, PasswordResetUrl, FriendsRequests


class InvitationUrlsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'expiration_date', 'tried',
                    'active', 'url_uuid')
    list_filter = ('date', )
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields = ('name', 'email')

    fieldsets = (
        ('Informations', {
            'fields': ('name', 'email', 'expiration_date', 'sender_user')
        }), )


class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'spec_url', 'key_nb')

    search_fields = ('user', 'key_nb')
    fieldsets = (
        ('Informations', {
            'fields': ('user', 'spec_url', 'key_nb')
        }), )


class FriendsRequestsAdmin(admin.ModelAdmin):
    list_display = ('sender_user', 'receiver_user', 'message', 'date')
    list_filter = ('date', )
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields = ('sender_user', 'receiver_user')

    fieldsets = (
        ('Informations', {
            'fields': ('sender_user', 'receiver_user', 'message', 'date')
        }), )


admin.site.register(InvitationUrls, InvitationUrlsAdmin)
admin.site.register(PasswordResetUrl)
admin.site.register(Keys)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(FriendsRequests, FriendsRequestsAdmin)
