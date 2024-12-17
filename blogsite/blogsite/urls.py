from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'), 
]

admin.site.site_header = 'Admin Panel'
admin.site.site_title = 'Super Admin Panel'
admin.site.index_title = 'Super Admin'