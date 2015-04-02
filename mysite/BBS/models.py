#!/usr/bin/python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from DjangoUeditor.commands import *
import datetime
from django.utils import timezone

#=========================== start ===========================================

def getImagePath(model_instance=None):
    if model_instance is None:
        return "aaa/"
    else:
        return "%s/" % model_instance.Name

def getDescImagePath(model_instance=None):
        return "aaa/"

class myEventHander(UEditorEventHandler):
    def on_selectionchange(self):
        return """
            function getButton(btnName){
                var items=%(editor)s.ui.toolbars[0].items;
                for(item in items){
                    if(items[item].name==btnName){
                        return items[item];
                    }
                }
            }
            var btn=getButton("mybtn1");
            var selRanage=id_Description.selection.getRange()
            btn.setDisabled(selRanage.startOffset == selRanage.endOffset);

        """

class myBtn(UEditorButtonCommand):
    def onClick(self):
        return u"""
            alert("爽!");
            editor.execCommand(uiName);
        """
    def onExecuteQueryvalueCommand(self):
        return """
            return 1;
        """
    def onExecuteAjaxCommand(self,state):
        if state=="success":
            return u"""
                alert("后面比较爽!"+xhr.responseText);
            """
        if state=="error":
            return u"""
                alert("讨厌，摸哪里去了！"+xhr.responseText);
            """
class myCombo(UEditorComboCommand):
    def onSelect(self):
        return u"""
            alert("选择了!");
        """
    def get_items(self):
        items=[]
        for i in xrange(10):
            items.append({
                "label":"combo_%s" % i,
                "value":i
            })
        return items


#=========================== end =============================================


class BbsContent(models.Model):
    SEX_SELECT=(('man','男'),('woman','女'),('kids','小孩'))
    title=models.CharField(max_length=36,verbose_name=u'标题')
    smarty=models.CharField(max_length=256,verbose_name=u'简介')
    image=models.ImageField(verbose_name='头像',upload_to='static/upload/content/',default='static/upload/head/xy.jpg')
    contents=UEditorField(u'描述', blank=True, toolbars="full", imagePath="static/upload/cool/", settings={"a": 1},
                               command=[myBtn(uiName="mybtn1", icon="d.png", title=u"1摸我", ajax_url="/ajaxcmd/"),
                                       myCombo(uiName="myCombo3",title=u"ccc",initValue="aaa")],
                               event_handler=myEventHander())
    category=models.ForeignKey('Category',verbose_name=u'类别')
    author=models.ForeignKey('BbsUser',verbose_name=u'发布者')
    view_count=models.IntegerField(default=0,verbose_name=u'查看次数')
    rank=models.IntegerField(default=0,verbose_name=u'赞')
    sex_old=models.CharField(max_length=5,choices=SEX_SELECT,verbose_name='年龄类别')
    top=models.BooleanField(verbose_name='是否置首页',default=False)
    create_time=models.DateTimeField(verbose_name=u'创建日期',default=datetime.datetime.now())
    update_time=models.DateTimeField(verbose_name=u'更新日期',auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    def was_published_recently(self):
        return self.registerDateTime >=timezone.now()-datetime.timedelta(days=1)
    class Meta:
        verbose_name=u'内容'
        verbose_name_plural=u'内容管理中心'
    
class Category(models.Model):
    category_name=models.CharField(verbose_name=u"类别",max_length=26)  
    def __unicode__(self):
        return self.category_name
    class Meta:
        verbose_name=u'类别'
        verbose_name_plural=u'类别管理中心'

class BbsUser(models.Model):
    user=models.OneToOneField(User,verbose_name=u"用户名")
    image=models.ImageField(verbose_name='头像',upload_to='static/upload/head/',default='static/upload/head/xy.jpg')
    bbs_rank=models.IntegerField(default=0,verbose_name=u'等级')
    def __unicode__(self):
        return self.user.username
    class Meta:
        verbose_name=u'用户'
        verbose_name_plural=u'用户管理中心'
        
class BbsUserAnswer(models.Model):
    answer_user=models.ForeignKey(BbsUser,verbose_name=u'用户名',blank=True,null=True)
    answer_bbs=models.ForeignKey(BbsContent,verbose_name=u'标题')
    answer_datetime=models.DateTimeField(verbose_name=u'回复时间')
    #answer_content=models.TextField(verbose_name=u'内容')
    answer_content = UEditorField(u'内容', height=200, width=800, default='test', imagePath="static/upload/answer/img/", toolbars="mini",
                           filePath='static/upload/answers/files/', blank=True, settings={"a": 2})
    def __unicode__(self):
        return self.answer_bbs.title
    class Meta:
        verbose_name=u'评论'
        verbose_name_plural=u'评论管理中心'
        
    