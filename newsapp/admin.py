from django.contrib import admin
from django.contrib.admin.decorators import action
from newsapp.models import *

# Register your models here.

class SourceAdmin(admin.TabularInline):
    model = Source

class AccountAdmin(admin.ModelAdmin):
   inlines = [SourceAdmin,]

admin.site.register(Account)
admin.site.register(Source)
admin.site.register(Newsfeed)