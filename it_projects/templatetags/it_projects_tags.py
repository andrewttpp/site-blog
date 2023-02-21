from django import template
from it_projects.models import *
from it_projects.views import menu

register = template.Library()


@register.simple_tag(name='getmenu')
def get_menu():
    return menu


@register.simple_tag(name='getbest')
def get_menu():
    best_posts = Projects.objects.all()
    return best_posts[0:3]


@register.inclusion_tag('it_project/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}
