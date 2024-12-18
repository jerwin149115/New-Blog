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
    path('post-detail/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit', views.edit_post, name='edit_post'),
    path('posts/<int:id>/delete', views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name="add_comment"),
    path('accounts/login/', views.LoginView.as_view(), name='login')
]


