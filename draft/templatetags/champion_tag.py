from django import template
from django.utils import timezone
import re, os, datetime

register = template.Library()

@register.filter
def sp_position(no):
    return -int(no)*82