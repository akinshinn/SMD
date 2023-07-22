from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name="login"),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('diary/', views.diary, name="diary"),
    path('portfolios/', views.portfolios, name="portfolios")
]
