from django.contrib import admin
from .models import Car, Comment


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'owner', 'created_at')
    search_fields = ('make', 'model', 'owner__username')
    list_filter = ('make', 'year')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'created_at')
    search_fields = ('content', 'author__username')
    list_filter = ('created_at',)
