# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import  render_to_response, redirect
from post.models import Post, City
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datetime_safe import datetime
from datetime import date, datetime, timedelta, time
import operator
from urlparse import urlparse
import urlparse
import pickle
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.template import RequestContext
from django.core.context_processors import csrf



startdate = date.today()
enddate = startdate + timedelta(days=365000)
key = 'my_qs'
REC_TO_PAGE = 10

count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))


def delete_posts(requsts):
    start = date.today() - timedelta(days = 10)
    end = startdate
    Post.objects.filter(post_deadline__range = [start, end] ).delete()


def delete_session(request):
    if "sort" in request.session:
      del request.session["sort"]
    if "city" in request.session:
        del request.session["city"]
    if "name_gift" in request.session:
        del request.session["name_gift"]
    if "category" in request.session:
        del request.session["category"]
    if "members_from" in request.session:
        del request.session["members_from"]
    if "members_to" in request.session:
        del request.session["members_to"]
    if "qty_gift_from" in request.session:
        del request.session["qty_gift_from"]
    if "qty_gift_to" in request.session:
        del request.session["qty_gift_to"]
    if "days_from" in request.session:
        del request.session["days_from"]
    if "days_to" in request.session:
         del request.session["days_to"]



# Главная страница
def posts(request, page_number = 1):
    delete_posts(request)
    delete_session(request)

    if "name_gift" in request.session:
        del request.session["name_gift"]

    now_posts = Post.objects.filter(post_deadline__range = [startdate, enddate]).order_by('-post_date')
    request.session[key] = pickle.dumps(now_posts.query)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(now_posts, REC_TO_PAGE)
    all_city = City.objects.order_by("-city_qty_posts")
    return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count_all, 'count_all': count_all, 'all_city': all_city
                                             }, context_instance=RequestContext(request))

'''
# Расширенный поиск
def find(request, page_number = 1):
    key = 'my_qs'
    city = request.POST['city']
    category = request.POST.getlist('category', [])
    members_from = request.POST['members_from']
    members_to = request.POST['members_to']
    qty_gift_from = request.POST['qty_gift_from']
    qty_gift_to = request.POST['qty_gift_to']
    days_from = request.POST['days_from']
    days_to = request.POST['days_to']

    request.session["city"] = city
    selected_city = request.session["city"]

    request.session["category"] = category
    selected_category = request.session["category"]

    if request.POST['members_from'] == u'':
        members_from = 1
        selected_members_from = ""
        request.session["members_from"] = ""
    else:
        request.session["members_from"] = members_from
        selected_members_from = request.session["members_from"]

    if request.POST['members_to'] == u'':
        members_to = 1000000
        selected_members_to = ''
        request.session["members_to"] = ''
    else:
        request.session["members_to"] = members_to
        selected_members_to = request.session["members_to"]

    if request.POST['qty_gift_from'] == u'':
        qty_gift_from = 1
        selected_qty_gift_from = ''
        request.session["qty_gift_from"] = ''
    else:
        request.session["qty_gift_from"] = qty_gift_from
        selected_qty_gift_from = request.session["qty_gift_from"]

    if request.POST['qty_gift_to'] == u'':
        qty_gift_to = 50
        selected_qty_gift_to = ''
        request.session["qty_gift_to"] = ''
    else:
        request.session["qty_gift_to"] = qty_gift_to
        selected_qty_gift_to = request.session["qty_gift_to"]

    if request.POST['days_from'] == u'':
        days_from = 1
        selected_days_from = ''
        request.session["days_from"] = ''
    else:
        request.session["days_from"] = days_from
        selected_days_from = request.session["days_from"]

    if request.POST['days_to'] == u'':
        days_to = 365
        selected_days_to = ''
        request.session["days_to"] = ''
    else:
        request.session["days_to"] = days_to
        selected_days_to = request.session["days_to"]

    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))

    date_from = startdate + timedelta(days=int(days_from))
    date_to = startdate + timedelta(days=int(days_to) + 1)
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session:
        posts = Post.objects.filter(post_name_gift__icontains=request.session["name_gift"], post_city = city,
                                    post_category__in = category, post_members__range = [members_from, members_to],
                                    post_qty_gifts__range = [qty_gift_from, qty_gift_to],
                                    post_deadline__range = [date_from, date_to]).order_by('-post_date')
        count = len(posts)
        current_page = Paginator(posts, REC_TO_PAGE)
        request.session[key] = pickle.dumps(posts.query)
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all,
                                                 'selected_city': selected_city, 'selected_category': request.session["category"],
                                                 'selected_members_from': selected_members_from, 'selected_members_to': selected_members_to,
                                                 'selected_qty_gift_from': selected_qty_gift_from, 'selected_qty_gift_to': selected_qty_gift_to,
                                                 'selected_days_from': selected_days_from, 'selected_days_to': selected_days_to,
                                                 'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    else:
        posts = Post.objects.filter(post_city = city, post_category__in = category, post_members__range = [members_from, members_to],
                                    post_qty_gifts__range = [qty_gift_from, qty_gift_to],
                                    post_deadline__range = [date_from, date_to]).order_by('-post_date')

    request.session[key] = pickle.dumps(posts.query)
    count = len(posts)
    current_page = Paginator(posts, REC_TO_PAGE)
    return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all,
                                             'selected_city': selected_city, 'selected_category': request.session["category"],
                                             'selected_members_from': selected_members_from, 'selected_members_to': selected_members_to,
                                             'selected_qty_gift_from': selected_qty_gift_from, 'selected_qty_gift_to': selected_qty_gift_to,
                                             'selected_days_from': selected_days_from, 'selected_days_to': selected_days_to, 'all_city': all_city})

'''
# Поиск
def search(request, page_number=1):
    name_gift = request.POST['name_gift']
    request.session["name_gift"] = name_gift

    city = request.POST['city']
    request.session["city"] = city

    category = request.POST['category']
    request.session["category"] = category

    if category == "Все категории":
        now_posts = Post.objects.filter(post_name_gift__icontains=name_gift, post_city=city).order_by('-post_date')
    else:
        if city == "Выберите город:":
            now_posts = Post.objects.filter(post_name_gift__icontains=name_gift, post_category=category).order_by('-post_date')
        else:
            now_posts = Post.objects.filter(post_name_gift__icontains=name_gift, post_category=category, post_city=city).order_by('-post_date')

    all_city = City.objects.order_by("-city_qty_posts")
    if len(now_posts) == 0:
        count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
        request.session[key] = pickle.dumps(now_posts.query)
        return render_to_response('posts.html', {'count': 0, 'count_all': count_all,
                                                 'selected_name_gift': name_gift,
                                                 'selected_category': request.session["category"],
                                                 'selected_city': city, 'all_city': all_city})
    else:
        count = len(now_posts)
        request.session[key] = pickle.dumps(now_posts.query)
        current_page = Paginator(now_posts, REC_TO_PAGE)
        count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all,
                                                 'selected_name_gift': name_gift, 'selected_category': category,
                                                 'selected_city': city,  'all_city': all_city})



# Сортировки
def sorted_members_up(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_members'), reverse=False)
    request.session["sort"] = "по участникам по возрастанию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session and "category" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session and "category" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session and "category" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})

def sorted_members_down(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_members'), reverse=True)
    request.session["sort"] = "по участникам по убыванию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})


def sorted_days_up(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_deadline'), reverse=False)
    request.session["sort"] = "по дням до завершения по возрастанию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(newlist, REC_TO_PAGE)
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"]
        , 'selected_name_gift': request.session["name_gift"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})

def sorted_days_down(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_deadline'), reverse=True)
    request.session["sort"] = "по дням до завершения по убыванию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(newlist, REC_TO_PAGE)
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})

def sorted_gifts_up(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_qty_gifts'), reverse=False)
    request.session["sort"] = "по количеству победителей по возрастанию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})

def sorted_gifts_down(request, page_number=1 ):
    posts = Post.objects.all()[:1]
    posts.query = pickle.loads(request.session[key])
    newlist = sorted(posts, key=operator.attrgetter('post_qty_gifts'), reverse=True)
    request.session["sort"] = "по количеству победителей по убыванию"
    count = len(posts)
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    current_page = Paginator(newlist, REC_TO_PAGE)
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    all_city = City.objects.order_by("-city_qty_posts")
    if "name_gift" in request.session and "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
    elif "city" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
         'selected_category': request.session["category"], 'all_city': all_city})
    elif "name_gift" in request.session:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_name_gift': request.session["name_gift"], 'selected_sort': request.session["sort"],'selected_category': request.session["category"], 'all_city': all_city})
    else:
        return render_to_response('posts.html', {'posts': current_page.page(page_number), 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})

def pagination(request, page_number = 1):
        all_city = City.objects.order_by("-city_qty_posts")
        if "sort" in request.session:
            posts = Post.objects.all()[:1]
            posts.query = pickle.loads(request.session[key])
            count = len(posts)
            count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
            if request.session["sort"] == "по участникам по возрастанию":
                newlist = sorted(posts, key=operator.attrgetter('post_members'), reverse=False)
                current_page = Paginator(newlist, REC_TO_PAGE)
            if request.session["sort"] == "по участникам по убыванию":
                newlist = sorted(posts, key=operator.attrgetter('post_members'), reverse=True)
                current_page = Paginator(newlist, REC_TO_PAGE)
            if request.session["sort"] == "по дням до завершения по возрастанию":
                newlist = sorted(posts, key=operator.attrgetter('post_deadline'), reverse=False)
                current_page = Paginator(newlist, REC_TO_PAGE)
            if request.session["sort"] == "по дням до завершения по убыванию":
                newlist = sorted(posts, key=operator.attrgetter('post_deadline'), reverse=True)
                current_page = Paginator(newlist, REC_TO_PAGE)
            if request.session["sort"] == "по количеству победителей по возрастанию":
                newlist = sorted(posts, key=operator.attrgetter('post_qty_gifts'), reverse=False)
                current_page = Paginator(newlist, REC_TO_PAGE)
            if request.session["sort"] == "по количеству победителей по убыванию":
                newlist = sorted(posts, key=operator.attrgetter('post_qty_gifts'), reverse=True)
                current_page = Paginator(newlist, REC_TO_PAGE)
            try:
                posts =  current_page.page(page_number)
            except PageNotAnInteger:
                posts =  current_page.page(1)
            except EmptyPage:
                posts =  current_page.page(current_page.num_pages)

            if "name_gift" in request.session and "city" in request.session:

                return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
                'selected_category': request.session["category"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
            elif "name_gift" in request.session:
                return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"],
                                                         'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
            elif "city" in request.session:
                return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'selected_city': request.session["city"],
                'selected_category': request.session["category"], 'all_city': all_city})
            else:
                return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_sort': request.session["sort"], 'all_city': all_city})
        else:
            posts = Post.objects.all()[:1]
            posts.query = pickle.loads(request.session[key])
            count = len(posts)
            count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
            current_page = Paginator(posts, REC_TO_PAGE)
            try:
                posts =  current_page.page(page_number)
            except PageNotAnInteger:
                posts =  current_page.page(1)
            except EmptyPage:
                posts =  current_page.page(current_page.num_pages)
            if "name_gift" in request.session and "city" in request.session:
                    return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_city': request.session["city"],
                    'selected_category': request.session["category"],'selected_name_gift': request.session["name_gift"], 'all_city': all_city})
            elif "city" in request.session:
                    return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all, 'selected_city': request.session["city"],
                    'selected_category': request.session["category"], 'all_city': all_city})
            elif "name_gift" in request.session:
                    return render_to_response('posts.html', {'posts': posts, 'count': count, 'count_all': count_all,
                                                          'selected_name_gift': request.session["name_gift"], 'selected_category': request.session["category"], 'all_city': all_city})
            else:
                return render_to_response('posts.html', {'posts': posts, 'count': count_all, 'count_all': count_all, 'all_city': all_city})

def about_us(request):
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    return render_to_response('about_us.html', {'count_all': count_all}, context_instance=RequestContext(request))

def contacts(request):
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    return render_to_response('contacts.html', {'count_all': count_all}, context_instance=RequestContext(request))

def for_admins(request):
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    return render_to_response('for_admins.html', {'count_all': count_all}, context_instance=RequestContext(request))

def search_url(request):
    search_url = request.POST['search_url']
    post = Post.objects.filter(post_url_post = search_url)
    city = City.objects.all()
    count_all = len(Post.objects.filter(post_deadline__range = [startdate, enddate]))
    num = len(post)
    cities = ['По всей России', 'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Самара', 'Челябинск', 'Омск',
              'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Волгоград', 'Воронеж', 'Саратов', 'Краснодар', 'Тольятти', 'Тюмень', 'Ижевск']
    return render_to_response('for_admins.html', {'search_post': num, 'count_all':count_all, 'url_post': search_url, 'cities': cities}, context_instance=RequestContext(request))

def add_contest(request):
    post_url_post = request.POST['post_url_post']
    post_name_gift = request.POST['post_name_gift'].encode('utf-8')
    post_category = request.POST['post_category']
    post_qty_gifts = int(request.POST['post_qty_gifts'])
    post_city = request.POST['post_city']
    post_deadline = request.POST['post_deadline']
    post = Post(post_url_post = 'post_url_post', post_name_gift = 'post_name_gift', post_category = 'post_category',
                post_qty_gifts = post_qty_gifts, post_city = 'post_city', post_deadline = 'post_deadline', post_status = 2)
    post.save()
