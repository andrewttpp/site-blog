from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Projects(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = AutoSlugField(default=None, unique=True, populate_from='title')
    header_text = models.TextField(blank=True, max_length=3000, verbose_name='Текст обложки поста')
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото поста')
    content = models.TextField(blank=True, verbose_name='Текст поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания поста')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения поста')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория поста')
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Автор поста')
    author_setting = models.ForeignKey('ProfileUser', on_delete=models.CASCADE, verbose_name='Настройки пользователя')
    name_button_next = models.CharField(max_length=40, default='Читать далее', verbose_name='Текст кнопки "Читать"')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk, 'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Имя категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class User(AbstractUser):
    email = models.EmailField(max_length=254, null=False, unique=True, verbose_name='E-mail')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.username})


class ProfileUser(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="profile")
    first_name = models.CharField(max_length=254, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', null=True)
    avatar_author = models.ImageField(upload_to='users_avatar/', default='users_avatar/default_user_avatar.png',
                                      verbose_name='Аватар пользователя', null=True)
    date_birthday = models.DateField(null=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDERS, verbose_name='Пол', null=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user_id': self.pk, 'username': self.user.username})


class Comments(models.Model):
    post = models.ForeignKey('Projects', on_delete=models.CASCADE, verbose_name='Статья')
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(max_length=2000, verbose_name='Текст комментария')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения комментария')

    def __str__(self):
        return self.content[0:200]


# TODO:triggred when User object is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(
            user=instance
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
