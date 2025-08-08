from rest_framework import serializers
from .models import *

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['image']

class AdSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'city', 'category', 'image']

    def get_image(self, obj):
        first_image = obj.images.first()
        return first_image.image.url if first_image else None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']
