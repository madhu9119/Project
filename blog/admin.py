from django.contrib import admin
from .models import Post,Comments
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status']
    list_filter=('status','author','publish')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['title','slug','author','body','publish','created','updated','status']
    prepopulated_fields={'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    lisr_display=('name','email','post','body','created','updated','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')

admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentAdmin)
