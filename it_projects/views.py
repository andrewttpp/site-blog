from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from it_projects.forms import *
from transliterate import *
from django.views.generic import ListView, DetailView, CreateView

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'support'},
        {'title': 'Войти', 'url_name': 'login'}]


class ProjectsHome(ListView):
    model = Projects
    template_name = 'it_project/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Projects.objects.filter(is_published=True)


def about(request):
    context = {'menu': menu, 'title': 'О сайте'}
    return render(request, 'it_project/about.html', context=context)


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'it_project/addpage.html'

def support(request):
    context = {'menu': menu, 'title': 'Страница обратной связи'}
    return render(request, 'it_project/about.html', context=context)


def login(request):
    context = {'menu': menu, 'title': 'Страница входа'}
    return render(request, 'it_project/about.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страницы не найдена</h1>')


class ShowPost(DetailView):
    model = Projects
    template_name = 'it_project/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class ProjectsCategory(ListView):
    model = Projects
    template_name = 'it_project/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['posts'][0].category)
        context['cat_selected'] = context['posts'][0].category.slug
        return context

    def get_queryset(self):
        return Projects.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)
