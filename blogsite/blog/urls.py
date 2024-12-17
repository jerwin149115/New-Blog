from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import index, RegisterView, LoginView, PostListView
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('posts/', lambda request: render(request, 'posts.html'), name='posts'),
    path('posts/post-detail/<int:id>/', views.post_detail, name='post_detail'),
    path('api/posts/', views.get_posts, name='get_posts'),
    path('api/posts/<int:pk>/', views.get_post, name='get_post'),
    path('api/posts/create', PostListView.as_view(), name='post-list'),
    path('add/', views.add_post, name='add_post'),
]

