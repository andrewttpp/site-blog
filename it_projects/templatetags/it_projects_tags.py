from django import template
from django.db.models import Count

from it_projects.models import *
from it_projects.views import menu

register = template.Library()


@register.simple_tag(name='getmenu')
def get_menu():
    return menu


@register.simple_tag(name='getbest')
def get_menu():
    best_posts = Projects.objects.filter(is_published=True)

    return best_posts[0:3]


# @register.simple_tag(name='post_user')
# def get_posts(username):


@register.inclusion_tag('it_project/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}
