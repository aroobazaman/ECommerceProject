# shop/serializers.py

from rest_framework import serializers
from .models import Product, Category
from rest_framework import serializers
from .models import UserToken


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'stock', 'available', 'created', 'updated', 'image']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products']

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ['user', 'access_token', 'refresh_token', 'created_at', 'expires_at']