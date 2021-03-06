import pickle
import base64
import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField


class TurnOn(models.Model):
  onOff = models.BooleanField()
  

class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()
  

class BackImage(models.Model):
  imagePath = models.FilePathField()
  pageNumber = models.IntegerField()
  
class FormInput(models.Model):
  pageNumber = models.IntegerField()
  inputType = models.CharField(max_length=45)
  left = models.FloatField()
  top = models.FloatField()
  width = models.FloatField()
  height = models.FloatField()
  option1 = models.CharField(max_length=45, blank=True, null=True)
  option2 = models.CharField(max_length=45, blank=True, null=True)
  option3 = models.CharField(max_length=45, blank=True, null=True)
  option4 = models.CharField(max_length=45, blank=True, null=True)
  option5 = models.CharField(max_length=45, blank=True, null=True)
  correctAnswer = models.TextField(blank=True, null=True)
  questionNumber = models.IntegerField()
  points = models.IntegerField(default=1)
  helpText = models.TextField(blank=True, null=True)
  helpLink = models.URLField(blank=True, null=True)
  

class Project(models.Model):
  title = models.CharField(max_length=100)
  dateTime = models.DateTimeField(auto_now_add=True, blank=True)
  backgroundImages = models.ManyToManyField(BackImage)
  formInputs = models.ManyToManyField(FormInput, blank=True, null=True)
  
  def __unicode__(self):
        return u'%s %s' % (self.title, self.dateTime)
    
  class Meta:
      ordering = ['dateTime', 'title']

class UserInfo(models.Model):
    user = models.ForeignKey(User)
    avatar = models.URLField(blank=True, null=True)
    projects = models.ManyToManyField(Project, blank=True, null=True)
    createOrOpen = models.CharField(max_length=45, blank=True, null=True)
    fileID = models.CharField(max_length=100, blank=True, null=True)


    def __unicode__(self):
      return u'%s' % (self.user)
    
        
        

class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CredentialsModel, CredentialsAdmin)