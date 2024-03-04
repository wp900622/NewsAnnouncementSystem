from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
# Create your views here.
from myapp import models
import math
page1 = 1
def index(request,pageindex=None):
    global page1
    pagesize = 8
    newsall = models.newsunit.objects.all().order_by('-id')
    datasize = len(newsall)
    totalpage = math.ceil(datasize/pagesize)
    if pageindex == None:
        page1 = 1
        newsunits = models.newsunit.objects.filter(enabled= True).order_by('-id')[:pagesize]
    elif pageindex == 1:
        start = (page1 - 2) * pagesize
        if(start >= 0):
            newsunits  = models.newsunit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
        page1 -= 1
    elif pageindex == 2:
        start = page1*pagesize
        if start < datasize:
             newsunits  = models.newsunit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
        page1+=1
    elif pageindex == 3:
        start = (page1 - 1) * pagesize
        newsunits = models.newsunit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
    currentpage = page1
    return render(request,"index.html", locals())

def detail(request,detailid=None):
    unit = models.newsunit.objects.get(id=detailid)
    category = unit.catego
    title = unit.title
    pubtime = unit.pubtime
    nickname = unit.nickname
    message = unit.message
    unit.press += 1
    unit.save()
    return render(request, "detail.html", locals())

def login(request):
    message = ""
    if request.method == "POST":
        name = request.POST['username'].strip()
        password = request.POST['password']
        user1 = authenticate(username=name,password = password)
        if user1 is not None:
            if user1.is_active:
                auth.login(request,user1)
                return redirect('/adminmain/')
            else:
                message = "帳號無法啟用"
        else:
            message="登入失敗"
    return render(request, "login.html" , locals())

def newsadd(request):
    message = ""
    category = request.POST.get('news_type',"")
    subject = request.POST.get('news_subject',"")
    editor = request.POST.get('news_editor',"")
    content = request.POST.get('news_content',"")
    ok = request.POST.get('news_ok', "")
    enabled = True
    if subject == "" or editor == "" or content == "":
        message="每一個欄位都要填寫"
    else:
        if ok == 'yes':
            enabled = True
        else:
            enabled = False
        unit = models.newsunit.objects.create(catego = category, nickname=editor, title=subject,
                                          message=content,enabled=enabled,press = 0)
        unit.save()
        return redirect('/adminmain/')
    return render(request,"newsadd.html",locals())

def logout(request):
    auth.logout(request)
    return redirect('/index')
def adminmain(request, pageindex=None):
    global page1
    pagesize = 8
    newsall = models.newsunit.objects.all().order_by('-id')
    datasize = len(newsall)
    totalpage = math.ceil(datasize/pagesize)
    if pageindex == None:
        page1 = 1
        newsunits = models.newsunit.objects.order_by('-id')[:pagesize]
    elif pageindex == 1:
        start = (page1 - 1) * pagesize
        if(start >= 0):
            newsunits  = models.newsunit.objects.order_by('-id')[start:(start+pagesize)]
        page1 -= 1
    elif pageindex == 2:
        start = (page1 + 1)*pagesize
        if start < datasize:
             newsunits  = models.newsunit.objects.order_by('-id')[start:(start+pagesize)]
        page1+=1
    elif pageindex == 3:
        start = (page1 - 1) * pagesize
        newsunits = models.newsunit.objects.order_by('-id')[start:(start+pagesize)]
    currentpage = page1
    return render(request,"adminmain.html", locals())

def newsedit(request, newsid=None, edittype=None):
    unit = models.newsunit.objects.get(id=newsid)
    categories = ["公告", "更新", "活動","其他" ]
    enabled = True
    if edittype == None:
        type = unit.catego
        subject = unit.title
        editor= unit.nickname
        message = unit.message
        ok = unit.enabled
    elif edittype == '1':
        category = request.POST.get("news_type","")
        subject = request.POST.get("news_subject","")
        editor = request.POST.get("news_editor","")
        content = request.POST.get("news_content","")
        ok = request.POST.get("news_ok","")
        if ok == "yes":
            enabled = True
        else:
            enabled = False
        unit.catego = category
        unit.nickname = editor
        unit.title = subject
        unit.message = content
        unit.enabled = enabled
        unit.save()
        return redirect('/adminmain/')
    return render(request, "newsedit.html", locals())

def delete(request, newsid=None, deletetype=None):
    unit = models.newsunit.objects.get(id=newsid)
    if deletetype == None:
        type = str(unit.catego.strip())
        subject = unit.title
        editor = unit.nickname
        content = unit.message
        date = unit.pubtime
    elif deletetype == '1':
        unit.delete()
        return redirect('/adminmain/')
    return render(request, 'newsdelete.html', locals())
