# -*- coding: utf-8 -*- 
# Create your views here.
from collection.main.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import datetime
import re

from collection.captcha import *
from django import forms
from catalogue.models import User_Catalogue
from main.models import User_Settings


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password) 
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def activate_user(request,username,arg):
    user=None
    try:
        user=User.objects.get(username=username)
    except:
        return render_to_response('main/registration.html',{'message':u"Ошибка активации!"})
    if (str(arg)==str(abs(str(user.date_joined).__hash__())) and not user.is_active):
        user.is_active=True
        #Создаем для пользователя настройки и пользовательский каталог по умолчанию
        user.save()
        catalogue = User_Catalogue()
        catalogue.user = user
        catalogue.save()
        settings = User_Settings()
        settings.user = user
        settings.default_catalogue = catalogue
        settings.theme = 1
        settings.save()
        user.save()
        return render_to_response('main/registration.html',{'message':u"Пользователь "+username+u" успешно активирован!"})
    else:
        return render_to_response('main/registration.html',{'message':u"Ошибка активации!"})


def new_user(request):
    if (request.method=='POST'):
        username = request.POST['username'][:30]
        password = request.POST['password'][:30]
        email = request.POST['email']
        errors=[]
        if (len(User.objects.filter(username=username))!=0):
            errors.append(u"Имя пользователя "+username+u" уже занято!")
        if (re.match(r'^[\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+$',email)):
            pass
        else:
            errors.append(email+u" не является валидным адресом электронной почты!")
        if (User.objects.filter(email=email).count()>0):
            errors.append(u"Пользователь с таким адресом электронной почты уже зарегистрирован!")
        if (re.match(r'^\w+$',username)):
            pass
        else:
            errors.append(username+u" не является валидным именем пользователя!")
        if (errors==[]):
            user=User.objects.create_user(username=username,password=password,email=email)
            user.is_active=False
            user.save()
            try:
                text=u"Внимание! Данное письмо было составлено автоматически - не следует на него отвечать!\nКто-то при создании учётной записи на нашем сайте указал ваш адрес электронной почты!\nЕсли это сделали не вы - ничего не делайте!\n\nИначе, проследуйте по этой ссылке: http://"+request.META["HTTP_HOST"]+"/activate_user/"+username+"/"+str(abs(str(user.date_joined).__hash__()))
                user.email_user(u"Активация аккаунта",text)
            except:
                user.delete()
                errors.append(email+u" не является валидным адресом электронной почты!")
                return render_to_response('main/registration.html',{'errors':errors})
            return render_to_response('main/registration.html',{'message':u"Пользователь "+username+u" успешно создан!\nДля завершения регистрации, пройдите по ссылке в письме, отправленном на адрес "+email})
        return render_to_response('main/registration.html',{'errors':errors})
    else:
        return render_to_response('main/registration.html',{'errors':[]})

def save_theme(request,theme):
    if (request.user.is_authenticated()):
        try:
            setting=None
            try:
                setting=User_Settings.objects.get(user=request.user)
                setting.theme=theme
            except:
                setting=User_Settings(user=request.user,theme=theme)
            setting.save()
        except:
            pass
    return HttpResponse("")
        
def save_profile(request):
    if (request.user.is_authenticated()):
        try:
            setting=None
            theme=0
            catalogue='C'
            try:
                theme=request.GET["theme"]
                catalogue=request.GET["catalogue"]
                catalogue_columns=request.GET["catalogue_columns"]
            except:
                return HttpResponse("")
            try:
                setting=User_Settings.objects.get(user=request.user)
                setting.theme=theme
                setting.catalogue=catalogue
                setting.catalogue_columns=catalogue_columns
            except:
                setting=User_Settings(user=request.user,theme=theme,catalogue=catalogue,catalogue_columns=catalogue_columns)
            setting.save()
        except:
            pass
    return HttpResponse("")

def get_user_settings(user):
    settings=Default_Setting()
    if (user.is_authenticated()):
        q=User_Settings.objects.filter(user=user)
        if (q.count()>0):
            settings=q[0]
    return settings

def list_articles(request):
    news = Article.objects.all().order_by('-pub_date')[:15]  
    return render_to_response('main/main.html', 
		{'news':news,'user':request.user,'profile':get_user_settings(request.user)}
	)


def list_comments(request,article_id):
    a=Article.objects.get(id=article_id)
    if (a != None):
        form=CommentPostForm()
        return render_to_response('main/comment.html', {'comments':a.comment_set.all(),'article_id':article_id,'user':request.user,'form':form})
    return "Strange error (article not found)!"

class CommentPostForm(forms.Form):
    comment_text = forms.CharField(max_length=100,widget=forms.Textarea,initial='Введите ваш комментарий...',
            min_length=0, required=True)
    captcha = CaptchaField(label='Verification',
            options={'fgcolor': '#ffffff', 'bgcolor': '#121212','num_lines':5,'line_weight':1})
    article_id=forms.IntegerField(required=True)

def add_comment(request):
        ar_id=request.GET["article_id"]
        form = CommentPostForm(request.GET)
        if form.is_valid():
            p=form.cleaned_data
            article=Article.objects.get(id=p["article_id"])
            author=None
            if (request.user.is_authenticated()):
                author=request.user
            new_comment=Comment(body=p["comment_text"], pub_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),author=author,article=article)
            new_comment.save() 
            return render_to_response('main/comment.html', {'comments':article.comment_set.all(),'article_id':p["article_id"],'user':request.user,'form':form})
        else:
            article=Article.objects.get(id=ar_id)
            return render_to_response('main/comment.html', {'comments':article.comment_set.all(),'article_id':ar_id,'user':request.user,'form':form})
    #except:
      #  return HttpResponse("Произошла ошибка!")

def add_idea(request):
    try:
        idea_text=request.POST["idea_text"]
    except:
        idea_text=""
    if (idea_text!=""):
        idea_text=idea_text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    try:
        idea_header=request.POST["idea_header"]
    except:
        return HttpResponseRedirect("/ideas/")
    idea=Idea(title=idea_header,body=idea_text,pub_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),author=request.user,reat=0,theme="")
    idea.save()
    return list_ideas(request)


class IdeaCommentPostForm(forms.Form):
    comment_text = forms.CharField(max_length=100,widget=forms.Textarea,initial='Введите ваш комментарий...',
            min_length=0, required=True)
    captcha = CaptchaField(label='Verification',
            options={'fgcolor': '#ffffff', 'bgcolor': '#121212','num_lines':5,'line_weight':1})
    idea_id=forms.IntegerField(required=True)

def add_idea_comment(request):
    idea_id=request.GET["idea_id"]
    form = IdeaCommentPostForm(request.GET)
    if form.is_valid():
        p=form.cleaned_data
        idea=Idea.objects.get(id=p["idea_id"])
        author=None
        if (request.user.is_authenticated()):
            author=request.user
        new_comment=Idea_Comment(body=p["comment_text"], pub_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),author=author,idea=idea)
        new_comment.save() 
        return render_to_response('main/idea_comment.html', {'comments':idea.idea_comment_set.all(),'idea_id':p["idea_id"],'user':request.user,'form':form})
    else:
        idea=Idea.objects.get(id=idea_id)            
        return render_to_response('main/idea_comment.html', {'comments':idea.idea_comment_set.all(),'idea_id':idea_id,'user':request.user,'form':form})
   

def check_and_mark_vote(ip,idea,reat):
    if (idea.idea_vote_set.filter(ip=ip[:15]).count()==0):
        vote=Idea_Vote(reat=reat, ip=ip[:15],date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),idea=idea)
        vote.save()
    else:
        return False
    return True

def idea_vote_up(request,idea_id):
    idea=Idea.objects.get(id=idea_id)
    if (idea!=None): 
        if (check_and_mark_vote(request.META["REMOTE_ADDR"],idea,1)):
            idea.reat+=1
            idea.save()
        return HttpResponse(idea.reat)
    return HttpResponse("")

def idea_vote_down(request,idea_id):
    idea=Idea.objects.get(id=idea_id)
    if (idea!=None):
        if (check_and_mark_vote(request.META["REMOTE_ADDR"],idea,-1)):
            idea.reat-=1
            idea.save()
        return HttpResponse(idea.reat)
    return HttpResponse("")

def list_idea_comments(request,idea_id):
    a=Idea.objects.get(id=idea_id)
    if (a != None):
        form=IdeaCommentPostForm()
        return render_to_response('main/idea_comment.html', {'comments':a.idea_comment_set.all(),'idea_id':idea_id,'user':request.user,'form':form})
    return "Strange error (idea not found)!"

def list_ideas(request):
    ideas = Idea.objects.all().order_by('-pub_date')[:15]
    return render_to_response('main/ideas.html', 
		{'ideas':ideas,'user':request.user,'profile':get_user_settings(request.user)}
	)
    
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    #return HttpResponse(html)

