from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('',views.view_post_list, name='list'),
    path('post/category/<int:id>/', views.view_post_list, name='category'),
    path('update/<int:id>/', views.view_update_post, name='update_post'),
    path('delete/<int:id>/', views.view_delete_post, name="delete_post"),
    path('<int:id>/', views.view_post_detail, name='detail'),
    path('create/', views.view_create_post, name='create_post')
]
