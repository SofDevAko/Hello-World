# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re, datetime

NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
USER_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')

class UserManager(models.Manager):
    def login_validator(self, data):
        errors = []
        if User.objects.filter(username=data['username']):
            myuser=User.objects.get(username=data['username'])
            temppass = myuser.password
            if bcrypt.checkpw(data['password'].encode(), temppass.encode()):
                success = []
                return success
            else:
                errors.append('Invalid password!')
        else:
            errors.append('There is no registered email address')
        return errors

    def register_validator(self, data):
        errors = []
        if User.objects.filter(username=data['username']):
            errors.append('This username address is already registered')
        if len(data['name']) < 1 or len(data['username']) < 1 or len(data['password']) < 1 or len(data['conpass']) < 1:
            errors.append('Please fill all the fields!')
        if not USER_REGEX.match(data['username']):
            errors.append("Your username should contain letters and numbers only!")
        if not NAME_REGEX.match(data["name"]):
            errors.append("Your name should contain letters only!")
        if len(data['username']) < 3:
            errors.append("Your username should contain at least 3 letters!")
        if len(data['name']) < 3:
            errors.append("Your name should contain at least 3 letters!")
        if len(data['password']) < 8:
            errors.append("Your password should contain 8 characters or more!")
        if not data['password'] == data['conpass']:
            errors.append("Password and confirmation password doesn't match")
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class TravelManager(models.Manager):
    def travel_validator(self, data):
        curdate = unicode(datetime.datetime.now().date())
        testdate = unicode(data['datestart'])
        testdate2 = unicode(data['dateend'])
        errors = []
        if len(data['description']) < 1 or len(data['destination']) < 1 or len(data['datestart'])<1 or len(data['dateend'])<1:
            errors.append('Please fill all the fields')
        if testdate < curdate or testdate2 < curdate:
            errors.append('You cannot enter a past date for a future appointment')
        if testdate2 <testdate:
            errors.append('End date should be later than start date!')
        return errors
    
    def travel_creator(self, data):
        errors = []
        return errors

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    datestart = models.CharField(max_length=255, default = '1-1-1')
    dateend = models.CharField(max_length=255, default = '1-1-1')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    users_who_attend = models.ManyToManyField(User, related_name="travels_attended")
    
    objects = TravelManager()