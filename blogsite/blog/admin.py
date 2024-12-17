from django.contrib import admin
from blog.models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'tags')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)