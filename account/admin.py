from django.contrib import admin
from .models import Profile, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birthday', 'avatar_image')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created')
