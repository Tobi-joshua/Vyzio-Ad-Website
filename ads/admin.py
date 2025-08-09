from django.contrib import admin
from .models import *


class AdImageInline(admin.TabularInline):  # or StackedInline for larger form
    model = AdImage
    extra = 1  # how many empty forms to show
    fields = ('image',)
    readonly_fields = ()
    can_delete = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_advertiser', 'phone', 'country')
    search_fields = ('username', 'email', 'phone', 'country')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon','description')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'city', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'city', 'is_active')
    search_fields = ('title', 'description', 'city', 'user__username')
    inlines = [AdImageInline] 


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'image')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'amount', 'method', 'status', 'created_at')
    list_filter = ('method', 'status')
    search_fields = ('user__username', 'ad__title')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad', 'buyer', 'seller', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('ad__title', 'buyer__username', 'seller__username')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('chat__ad__title', 'sender__username', 'text')
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return (obj.text[:50] + "...") if obj.text else "(Attachment only)"
    text_preview.short_description = "Message Preview"












admin.site.site_header = "Vyzio Ad Admin"
admin.site.site_title = "Vyzio Ad Admin Portal"
admin.site.index_title = "Welcome to the Vyzio Ad Administration Portal"
