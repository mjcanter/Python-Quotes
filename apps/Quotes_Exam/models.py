# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Users(models.Model):
	name = models.CharField(max_length=40)
	alias = models.CharField(max_length=40)
	email = models.CharField(max_length=38)
	pw_hash = models.CharField(max_length=225)
	DOB = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)


	def __unicode__(self):
		return "id: " + str(self.id) + ", email: " + self.email

class Quotes(models.Model):
	quote_by = models.CharField(max_length=40)
	quote_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(Users, related_name="user_quote")

class Favorites(models.Model):
	fav_user = models.ForeignKey(Users, related_name="user_fav")
	fav_quote = models.ForeignKey(Quotes, related_name="quote_fav")
