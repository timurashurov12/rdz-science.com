from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('login/',login_view,name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/',register,name='register'),
    
    # user
    path('user/<str:username>/', user_view, name='user'),
    path('user/<str:username>/<slug:category_slug>', user_view, name='user_blogs'),
    path('user/<str:username>/edit_user/',edit_user,name='edit_user'),
    path('user/<str:username>/edit_user/change_password/',change_password,name='change_password'),
    path('add_post/',add_post,name='add_post'),
    
    # blogs
    path('blogs/', blogs_view, name='blogs'),
    path('blog/<int:pk>/edit/', edit_blog, name='edit_blog'),
    path('delete_record/<int:pk>', delete_record, name='delete_record'),
    path('blog_detail/<int:pk>/', blog_detail, name='blog_detail'),
    path('blogs/<slug:category_slug>/', blogs_view, name='blogs_by_category'),

    # search
    path('search_result/', search_result, name='search_result'),

    # dowload file
    path('download_file/<int:pk>/', download_file, name='download_file'),
]