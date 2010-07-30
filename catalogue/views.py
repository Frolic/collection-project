# -*- coding: utf-8 -*- 
from collection.catalogue.models import *
from django.contrib.auth.models import User
from collection.main.views import get_user_settings

from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404


from collection.settings import MEDIA_ROOT
from main.views import get_user_settings
import datetime
import re
import os

def img_path2url(value):
    s=""
    try:
        s=str(value).replace(MEDIA_ROOT,"/")
    except:
          pass
    return s

def convert_coins(request):
    for a in Short_Coin.objects.all():
        a.foto_obverse=os.path.join(MEDIA_ROOT,"img/uploaded/"+os.path.basename(a.foto_obverse))
        a.foto_reverse=os.path.join(MEDIA_ROOT,"img/uploaded/"+os.path.basename(a.foto_reverse))
        a.save()

def show_catalogue(request, id):
    if id:
        request.session['id'] = id
    else:
        request.session['id'] = 0
    return render_to_response('catalogue/list.html',{'countries':Country.objects.all().order_by('name'),'metals':Metal.objects.all().order_by('name'),'serias':Seria.objects.all().order_by('name'),'user':request.user,'profile':get_user_settings(request.user)})

def FromGet(request,f,name,default):
    m=default
    try:
        m=f(request.GET[name])
        request.session[name]=m
    except:
        m=default
        if (request.GET.has_key(name)):
            request.session[name]=m
    return request.session.get(name,m)

def add_to_catalogue(request, coin_id):
    user_catalogue_id = get_user_settings(request.user).default_catalogue.id
    user_catalogue = User_Catalogue.objects.get(id=user_catalogue_id)
    coin = Short_Coin.objects.get(id=coin_id)
    user_catalogue.coins.add(coin)
    user_catalogue.save()
    return render_to_response('catalogue/list.html',{'countries':Country.objects.all().order_by('name'),'metals':Metal.objects.all().order_by('name'),'serias':Seria.objects.all().order_by('name'),'user':request.user,'profile':get_user_settings(request.user)})

def coin_info(request, coin_id):
    try:
        coin = Short_Coin.objects.get(id=coin_id)
    except User_Coin.DoesNotExist:
        raise Http404
    return render_to_response('catalogue/coininfo.htm',{'coin':coin})
 
def list_coins(request):
    id = int(request.session.get('id', 0))
    paginator = request.GET.get('page', 1)
    
    if (request.GET.has_key("clear")):
        request.session["country"]=-1
        request.session["metal"]=-1
        request.session["seria"]=-1
        request.session["denomination"]=""
        request.session["coinage"]=""
        request.session["page"]=0
        request.session["order1_name"]=""
        request.session["order1_how"]=""
        request.session["order2_name"]=""
        request.session["order2_how"]=""
        request.session["order3_name"]=""
        request.session["order3_how"]=""
    country = FromGet(request,int,"country",-1) 
    metal = FromGet(request,int,"metal",-1)
    seria = FromGet(request,int,"seria",-1) 
    denomination = FromGet(request,unicode,"denomination","")
    coinage = FromGet(request,int,"coinage","")
    page=FromGet(request,int,"page",0)
    
    
    if id:
        try:
            catalogue = User_Catalogue.objects.get(id=id)
        except User_Catalogue.DoesNotExist:
            raise Http404
        coins = catalogue.coins.all()
    else:
        coins=Short_Coin.objects.all()
        
    if (country>-1):
        coins=coins.filter(country=country)
    if (metal>-1):
        coins=coins.filter(metal=metal)
    if (seria>-1):
        coins=coins.filter(seria=seria)
    if (denomination!=''):
        coins=coins.filter(denomination__icontains=denomination)
    if (coinage!=''):
        coins=coins.filter(years_of_coinage__first_year__lte=coinage,years_of_coinage__last_year__gte=coinage).distinct()

    order1_name=FromGet(request,unicode,"order1_name","")
    order1_how=FromGet(request,unicode,"order1_how","")
    order2_name=FromGet(request,unicode,"order2_name","")
    order2_how=FromGet(request,unicode,"order2_how","")
    order3_name=FromGet(request,unicode,"order3_name","")
    order3_how=FromGet(request,unicode,"order3_how","")
    s="coins=coins.order_by("
    f=0
    if (order1_name!=""):
        s+="'"+order1_how+order1_name+"'"
        f=1
    if (order2_name!=""):
        if f:
            s+=","
        s+="'"+order2_how+order2_name+"'"
        f=1
    if (order3_name!=""):
        if f:
            s+=","
        s+="'"+order3_how+order3_name+"'"
        f=1
    s+=")"
    if (f):
        exec(s)
    else:
        coins=coins.order_by("id")

    view='catalogue/catalogue.html'
    settings = get_user_settings(request.user)
    if (settings.catalogue=='T'):
        view='catalogue/cataloguelist.html'
        
    paginator = Paginator(coins, 10).page(int(paginator))
    if coins.count():
        coins = coins[paginator.start_index()-1:paginator.end_index()]
    return render_to_response(view,{'coins':coins, 'user':request.user,\
                                     'profile':settings, 'page':paginator, 'id':id})
