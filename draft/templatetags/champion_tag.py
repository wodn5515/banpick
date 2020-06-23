from django import template
from django.utils import timezone
from draft.models import Draft
import re, os, datetime

register = template.Library()

line_dic = [
    'TOP','JG','MID','ADC','SUP'
]

@register.filter
def sp_position(no):
    return -int(no)*82

@register.simple_tag
def player_name(name, no):
    name_list = name.split('//')
    no = int(no)
    return '[' + line_dic[no] + ']' + name_list[no] if name_list[no] else line_dic[no]