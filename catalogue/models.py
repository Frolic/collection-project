# -*- coding: utf-8 -*- 
from django.db import models
from collection.settings import MEDIA_ROOT
from django.contrib.auth import models as auth
import os

COIN_FIELD_CHOICES = (
    ('', u'Сторона монеты'),
    ('obverse', u'Аверс'),
    ('reverse', u'Реверс')
)

class VarDate(object):
    def __init__(self, year,month=-1,day=-1):
        try:
            self.day = int(day)
            if (self.day<1 or self.day>31):
                raise("error")
        except:
            self.day=-1
        try:
            self.month = int(month)
            if (self.month<1 or self.month>12):
                raise("error")
        except:
            self.month=-1
        try:
            self.year = int(year)
        except:
            self.year=0    
    def __unicode__(self):
        s=""
        if (self.day>0):
            s+=str(self.day)
        if (self.month>0 or s!=""):
            if (s!=""):
                s+="."
            if (self.month>0):
                s+=str(self.month)
        if (s!=""):
            s+="."
        s+=str(self.year)
        return s

class VarDateField(models.Field):
    __metaclass__ = models.SubfieldBase    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super(VarDateField, self).__init__(*args, **kwargs)    
    def db_type(self):
        return 'char(12)'    
    def to_python(self, value):
        if isinstance(value, VarDate):
            return value
        if (value.count(";")):
            #Данные получены из базы
            args = value.split(";")
            return VarDate(*args)
        elif (value.count(".")):
            #Данные получены из админки
            args=value.split(".")
            args.reverse()
            return VarDate(*args)
        else:
            return VarDate(value,-1,-1)    
    def get_db_prep_value(self, value):
        return ";".join([str(value.year),str(value.month),str(value.day)])

# Create your models here.
class Seria(models.Model):
    name=models.CharField(max_length=150)    
    def __unicode__(self):
        return self.name
    
class Country(models.Model):
    name=models.CharField(u'Название страны', max_length=70)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'

class LifeCountry(models.Model):
    country = models.ForeignKey(Country, verbose_name = u'Страна')
    year_begin = VarDateField()
    year_end = VarDateField()
    def __unicode__(self):
        return u'%s (%s-%s)' % (self.country, self.year_begin, self.year_end)
    
class Mint(models.Model):
    name = models.CharField(u'Название', max_length=60, blank=True)
    mark = models.CharField(u'Знак', max_length=10, blank=True)
    country = models.ForeignKey(Country, verbose_name = u'Страна')
    mark_foto = models.ImageField(u'Фото знака', upload_to="./img/mint/", blank=True)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        verbose_name = u'Монетный двор'
        verbose_name_plural = u'Монетные дворы'    

class Artist(models.Model):
    first_name = models.CharField(u'Имя', max_length = 60)
    last_name = models.CharField(u'Фамилия', max_length = 60)
    mark = models.ImageField(upload_to="./img/markar/", blank=True)
    country = models.ForeignKey(Country, verbose_name = u'Страна')
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        verbose_name = u'Художник'
        verbose_name_plural = u'Художники' 

class Metal(models.Model):
    name=models.CharField(max_length=70)    
    def __unicode__(self):
        return self.name

class Year_Interval(models.Model):
    first_year=models.IntegerField()
    last_year=models.IntegerField()    
    class Meta:
        ordering = ['first_year']
    def __unicode__(self):
        if (self.first_year < self.last_year):
            return str(self.first_year)+"-"+str(self.last_year)
        else:
            return str(self.first_year)

class Main_info(models.Model):
    foto_edge = models.ImageField(upload_to="./img/uploaded/", blank=True)
    type_of_edge = models.CharField(max_length=40)
    text_edge = models.CharField(max_length=150, blank=True)
    dating = models.CharField(max_length=50, choices=(
        ('AD', 'Christian era'),
        ('BC', 'Before Christ'),
        ('AH', 'Muslim era'),
        ('SH', 'Solar year'),
        ('MS', 'Monarchic Solar era'),
        ('VS', 'Vikrama Samvat'),
        ('SE', 'Saka era'),
        ('BE', 'Buddhist era'),
        ('RS', 'Bangkok era'),
        ('CS', 'Chula-Sakarat era'),
        ('EE', 'Ethiopian era'),
        ('KE', 'Korean era'),
        ('AS', 'Javanese Aji Saka era'),
        ('FE', 'Fasli era'),
        ('JE', 'Jewish era'),
        ('R', 'Roman'),
    ))
    types = models.CharField(max_length=50, choices=(
        ('Regular', 'Regular'),
        ('Commemorative', 'Commemorative'),
        ('Test', 'Test'),
        ('Investment', 'Investment'),
    ))
    weight = models.IntegerField(blank=True)
    diameter = models.IntegerField()
    thickness = models.IntegerField(blank=True)
    quality = models.CharField(max_length=10, choices=(
        ('UNC', 'UNC'),
        ('B/U', 'B/U'),
        ('Proof', 'Proof'),
        ('Proof-like', 'Proof-like'),
        ('Reverse_frosted', 'Reverse_frosted'),
    ))
    fineness = models.IntegerField(blank=True)
    fine_metal_contant = models.IntegerField(blank=True)
    formula = models.CharField(max_length=30, blank=True)
    other = models.CharField(max_length=80, blank=True)
    metal1 = models.CharField(max_length=40, blank=True)
    fineness1 = models.IntegerField(blank=True)
    fine_metal_contant1 = models.IntegerField(blank=True)
    formula1 = models.CharField(max_length=30, blank=True)
    other1 = models.CharField(max_length=80, blank=True)
    metal2 = models.CharField(max_length=40, blank=True)
    fineness2 = models.IntegerField(blank=True)
    fine_metal_contant2 = models.IntegerField(blank=True)
    formula2 = models.CharField(max_length=30, blank=True)
    other2 = models.CharField(max_length=80, blank=True)
    metal3 = models.CharField(max_length=40, blank=True)
    fineness3 = models.IntegerField(blank=True)
    fine_metal_contant3 = models.IntegerField(blank=True)
    formula3 = models.CharField(max_length=30, blank=True)
    other3 = models.CharField(max_length=80, blank=True)
    mintage_unc = models.IntegerField(blank=True)
    mintage_b_u = models.IntegerField(blank=True)
    mintage_proof = models.IntegerField(blank=True)
    mintage_proof_like = models.IntegerField(blank=True)
    mintage_proof_fr = models.IntegerField(blank=True)
    form = models.CharField(max_length=30)
    axis = models.IntegerField()
    mint = models.ForeignKey(Mint)
    
    #field = models.ManyToManyField()
    
    artist = models.CharField(max_length=25, blank=True)
    ar_of_obverse = models.CharField(max_length=25, blank=True)
    ar_ob_mark = models.ImageField(upload_to="./img/markar/", blank=True)
    ar_of_reverse = models.CharField(max_length=25, blank=True)
    ar_av_mark = models.ImageField(upload_to="./img/markar/", blank=True)
    sculptors = models.CharField(max_length=25, blank=True)
    sc_of_obverse = models.CharField(max_length=25, blank=True)
    sc_ob_mark = models.ImageField(upload_to="./img/marksc/", blank=True)
    sc_of_reverse = models.CharField(max_length=25, blank=True)
    sc_re_mark = models.ImageField(upload_to="./img/marksc/", blank=True)
    
    themes =  models.TextField(max_length=90, blank=True)
    obverse = models.TextField(max_length=1000, blank=True)
    reverse = models.TextField(max_length=1000, blank=True)
    history = models.TextField(max_length=10000, blank=True)
    comments = models.TextField(max_length=600, blank=True)
    
class Short_Coin(models.Model):
    foto_obverse = models.ImageField(upload_to="./img/uploaded/")#os.path.join(MEDIA_ROOT,"img/uploaded/"))
    foto_reverse = models.ImageField(upload_to="./img/uploaded/")#os.path.join(MEDIA_ROOT,"img/uploaded/"))
    country = models.ForeignKey(LifeCountry)
    date_of_issue = VarDateField(blank=True)
    years_of_coinage = models.ManyToManyField(Year_Interval)
    seria = models.ForeignKey(Seria, blank=True)
    denomination = models.CharField(max_length=30)
    metal = models.ForeignKey(Metal)
    metal_type = models.CharField(max_length=50)
    main_info = models.ForeignKey(Main_info, blank=True)
    def __unicode__(self):
        return self.denomination+"("+unicode(self.date_of_issue)+")"
    
class User_Catalogue(models.Model):
    user = models.ForeignKey(auth.User)
    coins = models.ManyToManyField(Short_Coin)
    def __unicode__(self):
        return unicode(self.id)

