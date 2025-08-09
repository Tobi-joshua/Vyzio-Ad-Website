from django.contrib import admin
from .models import User, Category, Ad, AdImage, Payment


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


admin.site.site_header = "Vyzio Ad Admin"
admin.site.site_title = "Vyzio Ad Admin Portal"
admin.site.index_title = "Welcome to the Vyzio Ad Administration Portal"
