from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput

from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from my_site_django.settings import *
import datetime


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Projects
        fields = ['category', 'title', 'content', 'photo', 'header_text', 'name_button_next']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Классы в Python'}),
            'content': forms.Textarea(
                attrs={'cols': 70, 'rows': 20, 'placeholder': 'Введите текст вашей статьи...'}),
            'header_text': forms.Textarea(attrs={'cols': 50, 'rows': 10,
                                                 'placeholder': 'Содержимое данного поля '
                                                                'будет добавлено в обложку '
                                                                'вашего поста в ленте'}),
            'name_button_next': forms.TextInput(attrs={'placeholder': 'Например: Читать далее'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(error_messages={'required': 'Please choose a star rating'}, label='E-mail',
                               widget=forms.EmailInput(attrs={'class': 'authentication-field', 'placeholder': ' '}))
    password = forms.CharField(error_messages={'required': 'Please choose a star rating'}, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'authentication-field', 'placeholder': ' '}))

    error_messages = {'invalid_login': 'Неправильный логин или пароль', 'incomplete': 'Введите правильный пароль'}


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})

    username = forms.CharField(label='Ник',
                               widget=forms.TextInput(attrs={'class': 'registration-field', 'placeholder': ' '}),
                               error_messages={
                                   'required': 'Кажется вы пропустили это поле'})
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(
                                 attrs={'class': 'registration-field', 'placeholder': ' ', 'autofocus': 'None'}),
                             error_messages={
                                 'required': 'Кажется вы пропустили это поле'})
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'registration-field', 'placeholder': ' '}),
                                error_messages={
                                    'required': 'Кажется вы пропустили это поле'})
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'registration-field', 'placeholder': ' '}),
                                error_messages={
                                    'required': 'Кажется вы пропустили это поле'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class MyProfilesUpdate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Пол не выбран'

    GENDERS = [('', 'Не выбрано')] + ProfileUser.GENDERS

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'settings-field'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'settings-field'}),
                                required=False)
    avatar_author = forms.ImageField(label='Фото профиля', widget=forms.FileInput, required=False)
    gender = forms.ChoiceField(label='Пол', choices=GENDERS, required=False)
    date_birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=False)

    class Meta:
        model = ProfileUser
        fields = ('avatar_author', 'first_name', 'last_name', 'gender', 'date_birthday')


class SetPasswordForms(SetPasswordForm):

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        
