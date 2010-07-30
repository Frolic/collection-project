# -*- coding: utf-8 -*- 
from collection.main.models import *
from django.contrib import admin

admin.site.register(Article)
admin.site.register(Comment)

admin.site.register(Idea)
admin.site.register(Idea_Comment)
admin.site.register(User_Settings)
admin.site.register(Idea_Vote)