from django.urls import path

from .views import *

urlpatterns = [
    path('', ProjectsHome.as_view(), name='main'),
    path('about/', about, name='about'),
    path('addarcticle/', AddPage.as_view(), name='add_page'),
    path('support/', support, name='support'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ProjectsCategory.as_view(), name='category')
]
