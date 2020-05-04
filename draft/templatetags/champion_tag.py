from django import template
from django.utils import timezone
import re, os, datetime

register = template.Library()

@register.filter
def sp_position(no):
    return -int(no)*82

@register.simple_tag
def player_name(name, no):
    name_list = name.split('//')
    no = int(no)
    return name_list[no] if name_list[no] else str(no+1)+'번 소환사'