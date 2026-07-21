from django.contrib import admin
from .models import Category, Ad, AdImage


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'status', 'author', 'views_count', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')
    inlines = [AdImageInline]
