from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from it_projects.forms import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import EmailMessage
from .utils import *
from .tokens import account_activation_token


class ProjectsHome(DataMixin, ListView):
    model = Projects
    template_name = 'it_project/index_1.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context |= c_def
        return context

    def get_queryset(self):
        return Projects.objects.filter(is_published=True)


class AboutSite(DataMixin, ListView):
    model = Projects
    template_name = 'it_project/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        context |= c_def
        return context


class AddPage(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'it_project/addpage.html'
    success_url = reverse_lazy('main')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context |= c_def
        return context

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.author = self.request.user
        try:
            fields.author_setting = ProfileUser.objects.get(user_id=fields.author.pk)
            fields.save()
            messages.success(self.request, 'Статья была успешная опубликована')
            return super().form_valid(form)
        except:
            fields.save(commit=False)
            messages.error(self.request, 'Произошла непредвиденная ошибка. Статья не была опубликована')
            return redirect('main')


class SupportPage(DataMixin, ListView):
    model = Projects
    template_name = 'it_project/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница обратной связи')
        context |= c_def
        return context


class LoginPage(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'it_project/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход в аккаунт')
        context |= c_def
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Projects
    template_name = 'it_project/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Projects.objects.get(pk=self.kwargs['post_id'])
        c_def = self.get_user_context(title=data.title)
        context |= c_def
        return context


class ProjectsCategory(DataMixin, ListView):
    model = Projects
    template_name = 'it_project/index_1.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context["posts"][0].category),
                                      cat_selected=context['posts'][0].category.slug)
        context |= c_def
        return context

    def get_queryset(self):
        return Projects.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)


def is_activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Активация прошла успешно. Вы можете войти в свой аккаунт')
        return redirect('login')
    else:
        messages.error(request, 'Активационная ссылка не верна')
        return redirect('login')


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string('../templates/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    gen_email_message = list(to_email.split("@")[0])[0] + 5 * '*' + list(to_email.split("@")[0])[-1] + '@' + \
                        to_email.split("@")[-1]
    if email.send():
        messages.success(request,
                         f'Ссылка на активацию аккаунта была отправлена на почту {gen_email_message}. '
                         f'Проверьте папку "Спам"')
    else:
        message.error(request, f'Problem sending')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'it_project/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context |= c_def
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(self.request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(self.request, error)


def logout_user(request):
    logout(request)
    return redirect('login')


class MyProfile(DataMixin, LoginRequiredMixin, FormView):
    form_class = MyProfilesUpdate
    template_name = 'it_project/my_profile.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        context |= c_def
        return context

    def get_initial(self):
        initial = super(MyProfile, self).get_initial()
        initial = initial.copy()
        req = self.request.user
        data_table = ProfileUser.objects.get(user_id=req.pk)
        initial['first_name'] = data_table.first_name
        initial['last_name'] = data_table.last_name
        initial['avatar_author'] = data_table.avatar_author
        initial['gender'] = data_table.gender
        initial['date_birthday'] = str(data_table.date_birthday)

        return initial

    def form_valid(self, form):
        if self.request.method == 'POST':
            profile_form = MyProfilesUpdate(self.request.POST, self.request.FILES,
                                            instance=self.request.user.profile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(self.request, 'Ваш профиль был успешно сохранен')
            else:
                messages.error(self.request, 'Произошла ошибка')
            return redirect('my_profile')

        return super(MyProfile, self).form_valid(form)


class ShowUserProfile(DataMixin, DetailView):
    model = ProfileUser
    template_name = 'it_project/user_profile.html'
    context_object_name = 'user_profile'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post_user = Projects.objects.filter(author__username=self.kwargs['username'], is_published=True)
        count_post = len(post_user)
        c_def = self.get_user_context(menu=menu, post_user=post_user, count_post=count_post,
                                      title=f"Профиль пользователя {self.kwargs['username']}")
        context |= c_def
        return context

    def get_queryset(self):
        return ProfileUser.objects.filter(user__username=self.kwargs['username'])


class PasswordChange(DataMixin, LoginRequiredMixin, FormView):
    form_class = SetPasswordForms
    template_name = 'it_project/password_change.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('my_profile')

    def get_form_kwargs(self):
        kwargs = super(PasswordChange, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(menu=menu,
                                      title=f"Изменение пароля")
        context |= c_def
        return context

    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(self.request, 'Пароль был успешно изменен')
            else:
                messages.error(self.request, 'Произошла ошибка')

        return super(PasswordChange, self).form_valid(form)
