from django.contrib import admin
from netdev.models import *

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
   fields = ['views', 'creation_date']

class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'position', 'is_closed')

admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Message)
