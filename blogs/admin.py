from django.contrib import admin

from .models import BlogEntry


class BlogEntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogEntry, BlogEntryAdmin)
