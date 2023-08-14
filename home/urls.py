from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('diary/', views.diary, name="diary"),
    path('portfolios/', views.portfolios, name="portfolios"), 
    path('add-post/', views.addPost, name="add-post"),
    path('portfolios/edit-stock/<int:id>', views.editStockPage, name="editStock"),
    path('delete/<int:id>', views.deleteStockPage, name="deleteStock"),
    path('portfolios/show-portfolio/<int:id>', views.showPortfolioPage, name="showPortfolio"),
    path("delete-portfolio/<int:id>", views.deletePortfolioPage, name="deletePortfolio"),
    path("history", views.historyPage, name="history"),
    path("show-stock/<int:id>", views.showStockPage, name="showStock"),
    path("delete-sold-stock/<int:id>", views.deleteSoldStock, name="deleteSoldStock"),
    path('change-password/', views.change_password, name="changePassword"),
    
]
