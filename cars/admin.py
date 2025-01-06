from django.contrib import admin
from .models import Car, Comment


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
