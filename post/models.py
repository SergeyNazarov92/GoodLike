# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Post(models.Model):
	class Meta():
		db_table = 'post'

	# Столбцы в бд соответственно: картинка подарка, название подарка, url группы, кол-во участников,
	# кол-во подарков, город, дата окончания, дата вставки в бд, категория товара, url поста

	post_img_gift = models.TextField()
	post_name_gift = models.CharField(max_length=200)
	post_url = models.CharField(max_length=200)
	post_members = models.IntegerField(max_length=200)
	post_qty_gifts = models.IntegerField()
	post_city = models.CharField(max_length=200)
	post_deadline = models.DateField()
	post_date = models.DateTimeField()
	post_category = models.CharField(max_length=50)
	post_url_post = models.CharField(max_length=200)
	post_num_claver = models.IntegerField()

class City(models.Model):
	class Meta():
		db_table = 'city'

	# Столбцы в бд соответственно: город, кол-во постов с данным городом
	city_name = models.CharField(max_length=30)
	city_qty_posts = models.IntegerField(max_length=30)




