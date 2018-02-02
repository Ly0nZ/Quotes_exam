# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q
from django.contrib.sessions.models import *
# Create your views here.

def main(request):
	return render(request, 'projectapp/main.html')

def register(request):
	errors = []
	for key, val in request.POST.items():
		if len(val) == 0:
			errors.append("{} cannot be left blank".format(key))
	if len(request.POST['password']) < 8:
			errors.append("Password must be at least 8 characters.")

	if request.POST['password'] != request.POST['confirm-password']:
		errors.append("Passwords do not match.")

	if errors:
		for err in errors:
			messages.error(request, err)
		return redirect('/')

	else:
		try:
			User.objects.get(email=request.POST['email'])
			messages.error(request, "The email used is already associated with an account.")
			return redirect('/')
		except User.DoesNotExist:

			hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=request.POST['name'],\
								alias=request.POST['alias'],\
								email=request.POST['email'],\
								password = hashpw)
			request.session['user_id'] = user.id
			return redirect('/dashboard')

def login(request):
	errors = []
	try:
		user = User.objects.get(email = request.POST['email'])
		# b.crypt.checkpw(Given_password, stored_password)
		if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
			request.session['user_id'] = user.id
			return redirect('/dashboard')
		else:
			messages.error(request, "Login credentials are incorrect.")
			return redirect('/')
	
	except User.DoesNotExist:
		messages.error(request, "Email does not exist. Please try agin.")
		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def dashboard(request):
	current_user = User.objects.get(id=request.session['user_id'])
	q_quotes = Quote.objects.exclude(users=current_user)
	fav_quotes = Quote.objects.filter(users=current_user)
	context = {
		'current_user': current_user,
		'q_quotes': q_quotes,
		'fav_quotes': fav_quotes,
		}
	return render(request, 'projectapp/dashboard.html', context)

def addQuote(request):
	errors = []
 	for key, val in request.POST.items():
		if len(val) == 0:
			errors.append("Submission fields cannot be left blank")

	if errors:
		for err in errors:
			messages.error(request, err)
		return redirect('/dashboard')

	user = User.objects.get(id=request.session['user_id'])
			
 	new_author = Author.objects.create(name=request.POST['author'])
 	new_quote = Quote.objects.create(content=request.POST['content'], post_owner=user, author=new_author)
 	new_quote.save()
 
	return redirect('/dashboard')

def addFavorites(request, id):
	quote_add = Quote.objects.get(id=id)
	current_user = User.objects.get(id=request.session['user_id'])
	quote_add.users.add(current_user)
	#item_add.save()
	return redirect('/dashboard')

def removeFavorites(request, id):
	quote_remove = Quote.objects.get(id=id)
	current_user = User.objects.get(id=request.session['user_id'])
	quote_remove.users.clear()
	return redirect('/dashboard')

def userPosts(request, id):
	user = User.objects.get(id=id)
	posts = Quote.objects.filter(post_owner=user)
	count = posts.count()
	context = {
		'user': user,
		'posts': posts,
		'count': count,
	}

	return render(request, 'projectapp/users.html', context)