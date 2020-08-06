from django.contrib import admin
from .models import Image, Review


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'created')
    list_filter = ['created']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'post')