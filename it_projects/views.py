from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from it_projects.forms import *
from transliterate import *
from django.views.generic import ListView

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'support'},
        {'title': 'Войти', 'url_name': 'login'}]


class MainPageProjects(ListView):
    model = Projects
    template_name = 'it_project/index.html'
    context_object_name = 'posts'


def about(request):
    context = {'menu': menu, 'title': 'О сайте'}
    return render(request, 'it_project/about.html', context=context)


def addarcticle(request):
    posts = Projects.objects.all()
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['slug'] = transliterate(form.cleaned_data['title'])
            try:
                Projects.objects.create(**form.cleaned_data)
                return redirect('main')
            except:
                return form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    context = {'posts': posts, 'form': form, 'menu': menu, 'title': 'Добавить статью'}
    return render(request, 'it_project/addpage.html', context=context)


def support(request):
    context = {'menu': menu, 'title': 'Страница обратной связи'}
    return render(request, 'it_project/about.html', context=context)


def login(request):
    context = {'menu': menu, 'title': 'Страница входа'}
    return render(request, 'it_project/about.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страницы не найдена</h1>')


def show_post(request, post_slug):
    post = get_object_or_404(Projects, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.category_id,
    }

    return render(request, 'it_project/post.html', context=context)


def show_category(request, cat_slug):
    posts = Projects.objects.filter(category__slug=cat_slug)

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'title': 'Отображение по рубрикам',
               'cat_selected': cat_slug,
               }

    return render(request, 'it_project/index.html', context=context)
