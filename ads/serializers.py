from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon','description']


class CategoryListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        categories = [Category(**item) for item in validated_data]
        return Category.objects.bulk_create(categories)


class BulkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon','description']
        list_serializer_class = CategoryListSerializer


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image','image_url']


class AdsSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)  
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description', 'city', 'price', 'currency',
            'is_active', 'created_at', 'header_image_url', 'images', 'category'
        ]

class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['user', 'category', 'title', 'description', 'city', 'price','currency','is_active']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_advertiser', 'phone', 'country']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user