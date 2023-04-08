from django.db.models import Count

from .models import *

menu = [{'title': 'Войти', 'url_name': 'login'}, {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Обратная связь', 'url_name': 'support'}]


class DataMixin:
    paginate_by = 10
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        user_menu = menu.copy()
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

