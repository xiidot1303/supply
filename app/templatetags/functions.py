from django import template
from app.models import *

register = template.Library()


@register.filter
def cuttext(text):
    if text:
        if len(text) > 14:
            r_text = text[:15] + "..."
        else:
            r_text = text
        return r_text
    else:
        return ""
