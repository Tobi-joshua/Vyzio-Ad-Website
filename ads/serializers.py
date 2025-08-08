from rest_framework import serializers
from .models import *

class AdSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'city', 'category', 'image']




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class CategoryListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        categories = [Category(**item) for item in validated_data]
        return Category.objects.bulk_create(categories)

class BulkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']
        list_serializer_class = CategoryListSerializer


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdsSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'city', 'price', 'is_active', 'created_at', 'images']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class CategoryWithAdsSerializer(serializers.ModelSerializer):
    ads = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'ads']

    def get_ads(self, obj):
        ads = Ad.objects.filter(category=obj, is_active=True).order_by('-created_at')
        return AdsSerializer(ads, many=True).data
