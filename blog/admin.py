# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from blog.models import BlogPage

# Register your models here.
class BlogPageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(BlogPage, BlogPageAdmin)
