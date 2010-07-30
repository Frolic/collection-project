# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth import models as auth
from catalogue.models import User_Catalogue

class Default_Setting():
    def __init__(self):
        self.user=auth.AnonymousUser
        self.theme=0
        self.catalogue='C'
        self.catalogue_columns='FCIYSDM'

class User_Settings(models.Model):
    CATALOGUE_CHOICES = (
        ('C', 'Карточки'),
        ('T', 'Таблица')
    )
    user=models.ForeignKey(auth.User)
    theme=models.IntegerField()
    catalogue=models.CharField(max_length=1,choices=CATALOGUE_CHOICES,default='C')
    catalogue_columns=models.CharField(max_length=8,default='FCIYSDM')
    default_catalogue = models.ForeignKey(User_Catalogue)
    def __unicode__(self):
        return str(self.theme)

class Article(models.Model):
	title =  models.CharField(max_length=200)
	body =   models.TextField()
	pub_date = models.DateTimeField('date published')
	theme	= models.CharField(max_length=100)
	author   = models.ForeignKey(auth.User)

	def __unicode__(self):
		return self.title

	
	
class Comment(models.Model):
	body =   models.TextField()
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(auth.User,null=True)
	article = models.ForeignKey(Article)

	def __unicode__(self):
		return self.body


class Idea(models.Model):
	title =  models.CharField(max_length=200)
	body =   models.TextField()
	pub_date = models.DateTimeField('date published')
	theme	= models.CharField(max_length=100)
	author   = models.ForeignKey(auth.User)
	reat = models.IntegerField()

	def __unicode__(self):
		return self.title

	
	
class Idea_Comment(models.Model):
	body =   models.TextField()
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(auth.User,null=True)
	idea = models.ForeignKey(Idea)

	def __unicode__(self):
		return self.body

class Idea_Vote(models.Model):
    reat=models.IntegerField()
    ip=models.CharField(max_length=15)
    date=models.DateTimeField()
    idea=models.ForeignKey(Idea)

