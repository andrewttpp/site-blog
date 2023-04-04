from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', ProjectsHome.as_view(), name='main'),
    path('about/', AboutSite.as_view(), name='about'),
    path('add-arcticle/', AddPage.as_view(), name='add_page'),
    path('support/', SupportPage.as_view(), name='support'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('password-recovery/', PasswordChange.as_view(), name='password_recovery'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('post/<int:post_id>/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ProjectsCategory.as_view(), name='category'),
    path('my-profile/', MyProfile.as_view(), name='my_profile'),
    path('user/<int:user_id>/<username>', ShowUserProfile.as_view(), name='user_profile'),
    path('activate/<uidb64>/<token>', is_activate, name='activate')
]
