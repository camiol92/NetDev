from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from netdev.models import *

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
   fields = ['views', 'creation_date']

class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'position', 'is_closed')


class FileCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'pub_date', 'last_mod')
    search_fields = ('name',)

class RepoFileAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'description', 'public', 'pub_date')
    search_fields = ('name', 'category', 'description')
    #filter_horizontal =  ('allowed_users',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(FileCategory, FileCategoryAdmin)
admin.site.register(RepoFile, RepoFileAdmin)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(StatusUpdate)