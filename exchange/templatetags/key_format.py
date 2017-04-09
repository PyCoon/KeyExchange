#-*- coding:utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
register = template.Library()

@register.filter()
def key_format(key):
    key=0
    return mark_safe(key)
    
