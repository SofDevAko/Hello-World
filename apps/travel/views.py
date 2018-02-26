# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
import re, bcrypt, datetime
from django.contrib import messages
from .models import User, Travel
from time import strftime

def main(request):
    return render(request, 'travel/main.html')

def check(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        myuser=User.objects.get(username=request.POST['username'])
        request.session['active_username'] = myuser.username
        request.session['active_name'] = myuser.name
        request.session['active_id'] = myuser.id
        return redirect('/travels')

def create(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        User.objects.create(
            name = request.POST['name'],
            username = request.POST['username'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
        )
        messages.success(request, "You have successfully registered!")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    if 'active_id' in request.session:
        perstravels = Travel.objects.all().filter(users_who_attend = request.session['active_id'])
        alltravels = Travel.objects.all().exclude(users_who_attend = request.session['active_id'])
        context = { 
            'perstravels' : perstravels,
            'alltravels' : alltravels,
            }
        return render(request, 'travel/travels.html', context)
    else:
        messages.error(request, "You need to login first!")
        return redirect("/")

def addtravel(request):
    errors = Travel.objects.travel_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/travels/addform')
    else:
        user = User.objects.get(id=request.session['active_id'])
        travel = Travel.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            datestart = request.POST['datestart'],
            dateend = request.POST['dateend'],
            created_by = request.session['active_name'],
        )
        
        travel.users_who_attend.add(user)
        travel.save()
        messages.success(request, "You have successfully added an travel!")
        return redirect('/travels')

def addform(request):
    return render(request, 'travel/add.html')

def show(request, id):
    travel = Travel.objects.get(id = id)
    creator = travel.created_by
    creatorid = User.objects.get(name = creator)
    otherusers = User.objects.filter(travels_attended = id).exclude(id = creatorid.id).exclude(id = request.session['active_id'])
    context = { 
        'otherusers' : otherusers,
        'travel' : travel
        }
    return render(request, 'travel/destination.html', context)

def join(request, id):
    user = User.objects.get(id = request.session['active_id'])
    travel = Travel.objects.get(id = id)
    travel.users_who_attend.add(user)
    return redirect('/travels')