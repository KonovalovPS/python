from django.contrib import admin
from .models import User, Blogg, Post, Comment


admin.site.register(Blogg)
admin.site.register(Post)
admin.site.register(Comment)


# Register your models here.
