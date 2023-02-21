from django import forms
from .models import *


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
                                                                'вашего поста в ленте и '
                                                                'автоматически добавлено '
                                                                'в начало статьи'}),
            'name_button_next': forms.TextInput(attrs={'placeholder': 'Например: Читать далее'}),
        }
    # photo = forms.ImageField(label='Обложка поста')
