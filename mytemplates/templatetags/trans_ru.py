# -*- coding: utf-8 -*- 
from django import template
from collection.settings import MEDIA_ROOT
import os

register = template.Library()


@register.filter(name='tr_comment')
def tr_comment(value):
    try:
        i=int(value)
        if (i==0):
            return "нет комментариев"
        elif i>=10 and i<20:
            return str(value)+" комментариев"
        elif i%10==1:
            return str(value)+" комментарий"
        elif i%10<5 and i%10>0:
            return str(value)+" комментария"
    except:
          pass
    return str(value)+" комментариев"

@register.filter(name='img_path2url')
def img_path2url(value):
    s=""
    try:
        s=str(value).replace(os.path.realpath(MEDIA_ROOT),"").replace("//","/")
    except:
          pass
    return s

@register.filter(name='contains')
def contains(value, arg):
    return (value.count(arg)>0)

