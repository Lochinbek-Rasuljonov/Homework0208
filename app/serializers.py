from rest_framework import serializers
from .models import Blog, Comment, Category

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['category', 'name', 'text', 'image']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'blog']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']
        