# Create your views here.

from _datetime import datetime, timedelta

from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    context__dict = {"categories": Category.objects.order_by("-likes")[:5], }

    return render(request, 'rango/index.html', context=context__dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict["category"] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context_dict)
def current_time(request):
    t = datetime.now()
    t = t + timedelta(hours=3)
    context_dict = {"current_time": t, }
    return render(request, 'current_time.html', context=context_dict)
