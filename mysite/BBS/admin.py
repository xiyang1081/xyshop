#!/usr/bin/python
#coding=utf-8
from django.contrib import admin
from BBS import models

# Register your models here.
class BbsContentAdmin(admin.ModelAdmin):
    list_display=('title','smarty','category','author','rank','create_time','update_time')
    list_filter=('author__user__username','category','create_time')
    search_fields=('title','author__user__username')
    ordering=('-update_time',)

class BbsUserAdmin(admin.ModelAdmin):
    list_display=('user','bbs_rank','image')
    #list_filter=('user',)
    search_fields=('user',)
    ordering=('-user',)

class BbsUserAnswerAdmin(admin.ModelAdmin):
    list_display=('answer_bbs','answer_content','answer_datetime')
    list_filter=('answer_bbs','answer_bbs__author','answer_datetime')
    search_fields=('answer_bbs','answer_bbs__author')
    ordering=('-answer_datetime',)

admin.site.register(models.BbsContent,BbsContentAdmin)
admin.site.register(models.BbsUser,BbsUserAdmin)
admin.site.register(models.Category)
admin.site.register(models.BbsUserAnswer,BbsUserAnswerAdmin)
