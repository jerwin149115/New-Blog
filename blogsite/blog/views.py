from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm
from .serializers import PostSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def index(request):
    if request.user.is_authenticated:
        return redirect('posts')
    return render(request, 'index.html')


@login_required
def posts(request):
    return render(request, 'posts.html')


@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
        )
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # For form-based login, render the login form on GET requests
        form = AuthenticationForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        # Handle the POST request for user login via API
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Return a success response with tokens or redirect URL
            return Response({
                "redirect_url": "/posts/"
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post = Post.objects.get(id=id)
        if post.user != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=403)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=200)
    
    
@api_view(['GET'])
def get_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)
    
class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'author' not in request.data:
            request.data['author'] = request.user.id

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return JsonResponse({'error': 'You are not authorized to edit this post'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')

            if not title or not content:
                return JsonResponse({'error': 'Title and content cannot be empty'}, status=400)

            post.title = title
            post.content = content
            post.save()

            return JsonResponse({'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user:
        return JsonResponse({'error': 'You are not authorized to delete this post'}, status=403)
    
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True})

    return render(request, 'confirm_delete.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Empty content"})
    
    return redirect('post-detail', post_id=post.id)
