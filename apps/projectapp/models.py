# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)

class Author(models.Model):
	name = models.CharField(max_length=100)
	created_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)

class Quote(models.Model):
	content = models.TextField()
	author = models.ForeignKey(Author, related_name="author_quote")
	post_owner = models.ForeignKey(User, related_name="owner")
	users = models.ManyToManyField(User, related_name="users")
	created_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)