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
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_avatar_url = serializers.CharField(source='user.avatar_url', read_only=True)
    total_ads_posted = serializers.SerializerMethodField()
    member_since = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_country = serializers.CharField(source='user.country', read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description','user_country','city', 'price', 'currency','status',
            'is_active', 'created_at', 'header_image_url', 'images', 'category',
            'user_first_name', 'user_avatar_url', 'total_ads_posted',
            'member_since', 'average_rating'
        ]

    def get_total_ads_posted(self, obj):
        return Ad.objects.filter(user=obj.user).count()

    def get_average_rating(self, obj):
        return obj.user.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    def get_member_since(self, obj):
        return obj.user.date_joined.date() if obj.user.date_joined else None



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


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_name', 'text', 'created_at', 'is_read']


class ChatSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'ad', 'buyer', 'seller', 'buyer_name', 'seller_name', 'created_at']
