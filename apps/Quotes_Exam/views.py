# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, redirect
import random
import re
from django.contrib import messages
from django.db.models import Count, DateTimeField
from models import *
import bcrypt

def index(request):
	context = {
		"Users": Users.objects.all(),
		"Quotes": Quotes.objects.all()
		}
	return render(request, 'quotesexam/index.html', context)
def home(request):
	context = {
		"Users": Users.objects.all(),
		"curr_user": Users.objects.filter(id=request.session['userid']),
		"Quotes": Quotes.objects.all().exclude(quote_fav__fav_user__id=request.session['userid']),
		#"count": Quotes.objects.annotate(num_favs=Count('quote_favs')).order_by('num_favs'),
		"yourfavs": Quotes.objects.filter(quote_fav__fav_user__id=request.session['userid'])}
	return render(request, 'quotesexam/home.html', context)
def seluser(request):
   	context = {
		"Users": Users.objects.all(),
		"curr_user": Users.objects.filter(id=request.session['userid']),
		"sel_user": Quotes.objects.filter(user_id=Users.objects.get(id=request.POST['seluser'])),
	}
	print Users.objects.get(id=request.POST['seluser'])
	return render(request, 'quotesexam/seluser.html', context)

def register(request): 

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not request.POST['name']:
        messages.error(request, "Please enter your Name")
        return redirect("/")

    elif not request.POST['alias']:
        messages.error(request, "Please enter an Alias")
        return redirect("/")

    elif not request.POST['email']:
        messages.error(request, "Please enter an email")
        return redirect("/")
    elif not re.match(EMAIL_REGEX,request.POST['email']):
        messages.error(request, "Not a valid email")
        return redirect("/")
    elif Users.objects.filter(email=request.POST['email'])==True:
        messages.error(request, "Email is already in use")
        return redirect("/")

    elif not request.POST['password']:
        messages.error(request, "enter a password")
        return redirect("/")
    elif len(request.POST['password']) < 8:
        messages.error(request, "Password must be at least 8 characters")
        return redirect("/")
    elif request.POST['password'] != request.POST["confirm"]:
        messages.error(request, "Password must match")
        return redirect("/")
    else:
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Key =Users.objects.create(name=request.POST['name'],alias=request.POST['alias'],DOB=request.POST['dob'],email=request.POST['email'],pw_hash=hashed)
        request.session['userid'] = Key.id
        return redirect('/home')


def login(request):
    Key = Users.objects.get(email=request.POST['email'])
    storedhash = Key.pw_hash.encode('utf-8')
    inputdata = bcrypt.hashpw(request.POST['lgpassword'].encode('utf-8'), storedhash)
    if inputdata == storedhash:
    	request.session['userid'] = Key.id
    	print request.session['userid']
        return redirect('/home')
    else:
        messages.error(request, "User name or password not valid")
        return redirect('/')

def quote(request):
    if len(request.POST['quote_by']) < 4:
        messages.error(request, "Quoted By must be at least 4 characters")
        return redirect("/home")
    elif len(request.POST['new_quote']) < 11:
        messages.error(request, "Quoted must be more than 10 characters")
        return redirect("/home")
    else:    
		Quotes.objects.create(quote_text=request.POST['new_quote'], quote_by=request.POST['quote_by'],user_id=Users.objects.get(id=request.session['userid']))
		return redirect('/home')

def fav(request):
    print request.session['userid']
    Favorites.objects.create(fav_user=Users.objects.get(id=request.session['userid']),fav_quote=Quotes.objects.get(id=request.POST['fav_this'])),
    return redirect('/home')
def removefav(request):
    Favorites.objects.filter(fav_quote=Quotes.objects.get(id=request.POST['remove_this'])).delete()
    return redirect('/home')

#def delete(request):
#    print request.POST['delete_this']
#    Quotes.objects.get(id=request.POST['delete_this']).delete()
#    return redirect('/home')

def deleteuser(request):
    print request.POST['delete_this']
    Users.objects.get(id=request.POST['delete_this']).delete()
    return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')