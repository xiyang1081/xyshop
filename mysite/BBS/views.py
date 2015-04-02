#!/usr/bin/python
#coding=utf-8
import sys
reload(sys)
#sys.setdefaultencoding('utf-8')
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse,RequestContext
from django.shortcuts import HttpResponseRedirect
from BBS import models
from django.contrib.auth.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django import forms
from  DjangoUeditor.widgets import UEditorWidget
from django.contrib.auth.decorators import login_required

# Create your views here.
#======首页============================================================
def Index(request):
    #print request.user
    #if request.user.is_authenticated():
    #if request.COOKIES.get('username',''):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)
        #print 'username:',username
        #usernamecooks = request.COOKIES.get('username','')
        #print 'cooks:',usernamecooks
        
        #bbs_con=models.BbsContent.objects.all()
        """置于首页"""
        b=models.BbsContent.objects.filter(top=True).order_by('-update_time')[:8]
        #for bb in b:
            #print bb.title,bb.update_time
        
        return render_to_response('newbbs/index.html',{'bbs':b,'user':username})
    else:
        return HttpResponseRedirect('/login/')
    
#========详细列表========================================================================
def ShowList(request):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)
        #print 'username:',username
        #usernamecooks = request.COOKIES.get('username','')
        #print 'cooks:',usernamecooks
        """获取所有内容类表"""
        bbs_con=models.BbsContent.objects.all().order_by('-update_time')
        return render_to_response('newbbs/show-page.html',{'bbs':bbs_con,'user':username})
    else:
        return HttpResponseRedirect('/login/')

#========回复/评论=======================================================================
class DetailContentForm(forms.Form):
        bbs_answer_Content=forms.CharField(label=u"内容",
                              widget=UEditorWidget({"width":600, "height":100, "imagePath":'aa', "filePath":'bb', "toolbars":"full"}))

@csrf_exempt
def Detail(request,bbs_id):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)        
        bbs_detail=models.BbsContent.objects.get(id=bbs_id)
        #print bbs_detail.author
        bbs_user=models.BbsUser.objects.get(user__username=bbs_detail.author)
        #头像路径修改
        bbs_user.image='/media/'+str(bbs_user.image)        
        #回复列表
        answer=models.BbsUserAnswer.objects.filter(answer_bbs=bbs_id)
        
        if request.method=='POST' and request.POST.has_key('bbs_answer_Content') and request.POST['bbs_answer_Content'].strip()!='' :
            #print 'post:',request.POST
            #print request.POST['bbs_answer_Content']
            dcf=DetailContentForm(request.POST)
            #print "===",dcf
            if dcf.is_valid():
                anw_con=models.BbsUserAnswer()
                anw_con.answer_bbs=bbs_detail
                anw_con.answer_content=dcf.cleaned_data['bbs_answer_Content']
                anw_con.answer_datetime=datetime.datetime.now()
                anw_con.answer_user=models.BbsUser.objects.get(user=User.objects.filter(username=username))
                if not anw_con.save():
                    return HttpResponseRedirect('/detail/%s/' %(bbs_detail.id))
                else:
                    return render_to_response('newbbs/detail.html',{'detail':bbs_detail,
                                                                    'detail_head_img':bbs_user,
                                                                    'anw':answer,
                                                                    'user':username,
                                                                    'detail_error':'保存失败，请重试！'})
        return render_to_response('newbbs/detail.html',{'detail':bbs_detail,'detail_head_img':bbs_user,'anw':answer,'user':username})
    else:
        return HttpResponseRedirect('/login/')

#=========发布信息==================================================================

class InsertContentForm(forms.Form):
    bbs_contitle=forms.CharField(max_length=30)
    bbs_consmarty=forms.CharField(max_length=100)
    image=forms.ImageField()
    bbs_content=forms.CharField(label=u"内容",
                              widget=UEditorWidget({"width":600, "height":100, "imagePath":'aa', "filePath":'bb', "toolbars":"full"}))
    bbs_category=forms.CharField(max_length=20)
    sex_old=forms.CharField(max_length=5)
    #top=forms.BooleanField()
    
@csrf_exempt
def InsertContent(request):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)

        category=models.Category.objects.all()
        
        if request.method=='POST':
            #print 'POST:',request.POST
            uf=InsertContentForm(request.POST,request.FILES)
            if uf.is_valid():
                bbsContent=models.BbsContent()
                bbsContent.author=models.BbsUser.objects.get(user=User.objects.filter(username=username))
                bbsContent.title=uf.cleaned_data['bbs_contitle']
                bbsContent.smarty=uf.cleaned_data['bbs_consmarty']
                bbsContent.contents=uf.cleaned_data['bbs_content']
                bbsContent.image=uf.cleaned_data['image']
                bbsContent.category=models.Category.objects.get(category_name=uf.cleaned_data['bbs_category'])
                sex_old=uf.cleaned_data['sex_old']
                sextotle={u'男':'man',u'女':'woman',u'小孩':'kids'}
                sex_old=sextotle[sex_old]
                bbsContent.sex_old=sex_old
                
                bbsContent.top=False
                if request.POST['top']:
                    bbsContent.top=True                
                bbsContent.save() 
                return HttpResponseRedirect('/write/', {'user':username,'category':category})
            else:
                return HttpResponseRedirect('/write/', {'user':username,'category':category})
        return render_to_response('newbbs/insertcontent.html', {'user':username,'category':category})
    else:
        return HttpResponseRedirect('/login/')
    
#=========注册===========================================================
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=26)
    password=forms.CharField(max_length=26)
    email=forms.EmailField()
    image=forms.ImageField()
    firstname=forms.CharField(max_length=26)
    lastname=forms.CharField(max_length=26)


def Register(request):
    if request.method=='POST':
        print request.POST
        rf=RegisterForm(request.POST,request.FILES)
        print rf,"rf.is_valid()===",rf.is_valid(),rf.cleaned_data['image']
        if rf.is_valid():
            rg_user=User()
            rg_bbs_user=models.BbsUser()
            print '=============================================================='
            rg_user.username=rf.cleaned_data['username']
            rg_user.password=rf.cleaned_data['password']
            rg_user.email=rf.cleaned_data['email']
            rg_user.first_name=rf.cleaned_data['firstname']
            rg_user.last_name=rf.cleaned_data['lastname']
            rg_user.date_joined=datetime.datetime.now()
            print "rg_user:",rg_user
            rg_user.save()
            if rg_user.id:                
                rg_bbs_user.image=rf.cleaned_data['image']
                rg_bbs_user.user=rg_user
                rg_bbs_user.bbs_rank=0
                rg_bbs_user.save()
                if rg_bbs_user.id:
                    request.session['username'] = rg_user.username
                    response=HttpResponseRedirect('/')
                    response.set_cookie('username',rg_user.username,3600)
                    return response
                else:
                    del_user=User(id=rg_bbs_user.id)
                    del_user.delete()
                    return HttpResponseRedirect('/register/', {'error':'保存失败,请重试!'})
            else:
                return render(request,'newbbs/register.html',{'error':"保存失败，请重试！"})
    return render(request,'newbbs/register.html')

#=========登录===========================================================
@csrf_exempt
def Login(request):
    if request.method=='POST' and request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST['username']
        password = request.POST['password']
        #print username,password
        #result_login=models.BbsUser.objects.filter(user__username=username,user__password=password)
        #print 'result_login',result_login

        user = authenticate(username=username, password=password)
        print 'user:',user
        bbs_user=models.BbsUser.objects.filter(user=user)
        print "bbs_user",bbs_user
        if bbs_user:
            if user.is_active:
                #login(request, user)
                
                request.session['username'] = username
                response=HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                    #request.session
                    # Redirect to a success page.
                return response
            else:
                return render(request,'newbbs/login.html',{'error':"此用户未激活"})
        else:
            return render(request,'newbbs/login.html',{'error':"用户名或密码有误，请重试！"})
    return render(request,'newbbs/login.html')

#====登出=======================================================================
@login_required
def LoginOut(request):
    #print 'user:',request.user,request.session['username']
    del request.session['username']  #删除session
    response=HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    #logout(request.user)
    return response


#============验证码=============================================================
import cStringIO
import ImageFont,Image,ImageDraw
import random


def verify_code(request):
    background=(random.randrange(230,255),random.randrange(230,255),random.randrange(230,255))#随机靠山色彩
    line_color=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))#随机干扰色彩
    img_width=58
    img_height=30
    font_color=['darkred','black','darkblue']
    font_size=14
    string={'number':'123456789','litter':'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
    font=ImageFont.truetype('msyh.ttf',font_size,)
    request.session['verify']=''
    
    #新建画布
    im=Image.new('RGB',(img_width,img_height),background)
    draw=ImageDraw.Draw(im)
    code=random.sample(string['litter'],4)
    #新建画笔
    draw=ImageDraw.Draw(im)
    #干扰线
    for i in range(random.randrange(3,5)):
        xy=(random.randrange(0,img_width),random.randrange(0,img_height),random.randrange(0,img_width),random.randrange(0,img_height))
        draw.line(xy, fill=line_color, width=1)
    
    #写入验证码文字
    x=2
    for i in code:
        y=random.randrange(0,10)
        draw.text((x,y), i, fill=random.choice(font_color))
        x+=14
        request.session['verify']+=i
    del x
    del draw
    buf=cStringIO.StringIO()
    im.save(buf,'gif')
    buf.seek(0)
    return HttpResponse(buf.getvalue(),'image/fig')

#========关于================================================================

def About(request):
    return render(request,'newbbs/about.html')