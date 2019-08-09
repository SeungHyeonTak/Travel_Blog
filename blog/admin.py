from django.contrib import admin
from .models import *


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    list_display_links = ['title']


@admin.register(Maplocation)
class MaplocationAdmin(admin.ModelAdmin):
    list_display = ['placename', 'address']
    list_display_links = ['placename']
