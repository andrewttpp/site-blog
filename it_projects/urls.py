from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageProjects.as_view(), name='main'),
    path('about/', about, name='about'),
    path('addarcticle/', addarcticle, name='add_page'),
    path('support/', support, name='support'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:cat_slug>/', show_category, name='category')
]
