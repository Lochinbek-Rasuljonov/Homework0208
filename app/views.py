from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Comment, Category
from .serializers import BlogSerializer, CommentSerializer



class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

class HomeAPIView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        return Response({'blogs': [blog.name for blog in blogs]})


class BlogDetailAPIView(APIView):
    
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        comments = blog.comments.all()
        return Response({
            'blog': blog.name,
            'comments': [comment.text for comment in comments]
        })
    
    def post(self, request, blog_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            blog = get_object_or_404(Blog, id=blog_id)
            serializer.save(blog=blog, user=request.user)
            return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id, comment_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        blog = get_object_or_404(Blog, id=blog_id)
        comment = get_object_or_404(Comment, id=comment_id, blog=blog)
        
        if comment.user != request.user:
            return Response({'error': 'You are not authorized to delete this comment'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class DeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user or request.user.is_superuser:
            comment.delete()
            return Response({'message': 'Comment deleted successfully'})
        return Response({'error': 'Permission denied'}, status=403)


class CategoryBlogsAPIView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        blogs = Blog.objects.filter(category=category)
        return Response({'category': category.name, 'blogs': [blog.name for blog in blogs]})

class SignupAPIView(APIView):
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'User registered successfully'})
        return Response({'error': form.errors}, status=400)