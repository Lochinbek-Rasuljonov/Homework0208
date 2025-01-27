from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import BlogViewSet, CommentViewSet, HomeAPIView, BlogDetailAPIView, DeleteCommentAPIView, CategoryBlogsAPIView, SignupAPIView

router = DefaultRouter()
router.register(r'v1/blogs', BlogViewSet)
router.register(r'v1/comments', CommentViewSet)

urlpatterns = [
    path('', lambda request: redirect('home-api')),
    path('api/v1/home/', HomeAPIView.as_view(), name='home-api'),
    path('api/v1/blog/<int:blog_id>/', BlogDetailAPIView.as_view(), name='blog-detail-api'),
    path('api/v1/comment/delete/<int:comment_id>/', DeleteCommentAPIView.as_view(), name='delete-comment-api'),
    path('api/v1/category/<int:category_id>/blogs/', CategoryBlogsAPIView.as_view(), name='category-blogs-api'),
    path('api/v1/signup/', SignupAPIView.as_view(), name='signup-api'),
    path('api/', include(router.urls)),
]
