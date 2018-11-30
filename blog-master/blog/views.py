from django.shortcuts import render,HttpResponse,redirect
import json
from django.contrib import auth
from blog import models
from blog import forms
from blogCMS import settings
from django.db.models import Count,Sum
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import F
from django.db import transaction
from django.http import JsonResponse
from blog.geetest import GeetestLib

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"



from blog.forms import *        #着了放的都是form组件里的东西

# 登录
def login(request):
    if request.method=="POST":
        print("====可以走过来")
        username = request.POST.get("username")
        password = request.POST.get("password")
        validCode = request.POST.get("valid_code")

        login_response = {"is_login": False, "error_msg": None}

        if validCode.upper()==request.session.get("keepValidCode").upper():          #验证码不区分大小写
            user = auth.authenticate(username=username,password=password)
            if user:
                login_response["is_login"]=True      #验证通过
                auth.login(request,user)

                # request.session["username"] = username
            else:
                login_response["error_msg"]="用户名或密码错误"   #验证不通过
        else:
            login_response["error_msg"]="验证码输入有误"         #验证码错误
        import json
        return HttpResponse(json.dumps(login_response))
    else:
        return render(request,"login.html")

# 注销
def log_out(request):
    auth.logout(request)
    return redirect("/login/")



# 生成验证码函数
def get_validCode_img(request):
    from io import BytesIO
    import random
    from PIL import Image,ImageDraw,ImageFont
    img = Image.new(mode="RGB", size=(120, 40),color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))   #背景
    draw = ImageDraw.Draw(img,mode="RGB")     #生成一个画笔，可以写东西
    draw.point([100, 20], fill="black")         #画点-----（坐标，参数）
    draw.line((5,20,90,30),fill="black")        #画线-----（开始坐标，结束坐标；颜色参数）
    draw.line((10,20,50,30),fill="black")
    draw.arc((60,0,68,8),0,90,fill="red")      #画圆------（xxxxxxxxx）
    draw.arc((0,0,80,40),0,90,fill="red")
    font = ImageFont.truetype("blog/static/font/kumo.ttf",25)
    draw.text([20,10],"python","purple",font=font)       #写文本  ----（坐标，文本，颜色，字体）
    valid_list = []
    for i in range(5):
        '''文本信息'''
        random_num = str(random.randint(0,9))
        random_lower_char = chr(random.randint(65,90))
        random_upper_char = chr(random.randint(97,122))
        random_char = random.choice([random_num,random_lower_char,random_upper_char])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)     #写一次添加一次


    f = BytesIO()
    img.save(f,"png")    #刷到内存
    data = f.getvalue()   #从内存取值
    ########################################################################
    valid_str = "".join(valid_list)   #将列吧拼接成字符串
    print(valid_str)
    request.session["keepValidCode"]=valid_str       #存到session中
    return HttpResponse(data)


# 注册
def reg(request):
    if request.method == "POST":
        print(request.FILES)
        regform = RegForm(request,request.POST,request.FILES)
        # print("=====这里是regform=====")

        reg_response = {"user":None,"valid_code":False,"errors":""}
        # print(regform.cleaned_data.get("username"))
        if regform.is_valid():
            print("===this is ===")
            username = regform.cleaned_data.get("username")
            password = regform.cleaned_data.get("password")

            obj = models.UserInfo.objects.create_user(username=username,password=password,avatar=request.FILES.get("img","/avatar/default.png"))
            reg_response["user"]=username
            print("======", reg_response["user"])
        else:
            print("===验证不通过====")
            reg_response["errors"]=regform.errors

        # return HttpResponse("OK")
        return HttpResponse(json.dumps(reg_response))

    regform = RegForm(request)
    return render(request,"reg.html",{"regform":regform})


# def reg(request):
#     import json
#     if request.method == "POST":
#         print("=======>",request.POST)
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         nickname = request.POST.get("nickname")
#         telephone = request.POST.get("telephone")
#         print("===>",username)
#         response = {"flag":False}
#         if models.UserInfo.objects.filter(username=username):
#             response["flag"] = True
#         else:
#             models.UserInfo.objects.create(username=username,password=password,nickname=nickname,telephone=telephone)
#         return HttpResponse(json.dumps(response))
#
#         # form = RegForm(data=request.POST)
#         # print("====>",request.POST.get("avatar"))
#         # if form.is_valid():
#         #     print("======","这里？")
#         #     models.UserInfo.objects.create(**form.cleaned_data)
#         #     return HttpResponse("添加成功")
#         # print("---------------------",form.errors)
#         # return HttpResponse("验证不通过,没插入数据")
#     else:
#         reg_form = forms.RegForm()
#         return render(request,"reg.html",{"reg_form":reg_form})

# 文章
def article(request):
    return render(request,"article.html")


def comment(request):
    return HttpResponse("这里具有你的所有权限")




def index(request,*args,**kwargs):
    print(kwargs)
    if kwargs:
        article_list = models.Article.objects.filter(site_article_category__name=kwargs.get("site_article_category"))
        print("=====>",article_list)
    else:
        article_list = models.Article.objects.all()
    cate_list = models.SiteCategory.objects.all()

    #    分页相关
    paginator = Paginator(article_list, 3)
    page_range = paginator.page_range
    num = request.GET.get("page", 1)
    article_list = paginator.page(num)


    return render(request,"index.html",locals())



def homeSite(request,username,**kwargs):
    current_user = models.UserInfo.objects.filter(username=username).first()     #当前用户
    current_blog = current_user.blog          #反向查询到博客表

    if not current_user:
        return render(request,"notFound.html")

    # 分类归档    通过category表过滤出当前用户的站点，聚合查询反向
    category_list = models.Category.objects.all().filter(blog=current_blog).annotate(c=Count("article__nid")).values_list("title","c")
    #  标签归档   通过标签过滤出当前用户的站点，聚合反向查询
    tag_list = models.Tag.objects.all().filter(blog=current_blog).annotate(c=Count("article__nid")).values_list("title","c")
    # # 日期归档
    data_list = models.Article.objects.filter(user=current_user).extra(select={"filter_create_date":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("nid"))

    if kwargs:
        if kwargs.get("condition")=="category":
            article_list=models.Article.objects.filter(user=current_user,category__title=kwargs.get("para"))
        elif kwargs.get("condition") == "tag":
            article_list = models.Article.objects.filter(user=current_user, tags__title=kwargs.get("para"))
        elif kwargs.get("condition") == "date":
            year, month = kwargs.get("para").split("/")
            article_list = models.Article.objects.filter(user=current_user, create_time__year=year,create_time__month=month)


    if kwargs.get("article_id"):
        print("======>",request.path)
        user_obj = request.user
        article_obj = models.Article.objects.filter(nid=kwargs.get("article_id")).first()
        comment_obj_list = article_obj.comment_set.all()
        obj = render(request,"article_deatil.html",locals())
        obj.set_cookie("next_path",request.path)
        print(request.COOKIES.get("next_path"),"======================>")

        return obj
    else:
        article_list = models.Article.objects.filter(user=current_user)
        paginator = Paginator(article_list, 3)
        page_range = paginator.page_range
        num = request.GET.get("page", 1)
        article_list = paginator.page(num)
        
        return render(request,"homeSite.html",locals())







def up_count(request):
    '''点赞函数，禁止同一用户点赞多次'''
    user_id = request.user.nid                   #当前用户的ID
    article_id = request.POST.get("article_id")  # 获取到当前的文章ID
    print("===================点赞")
    pollResponse = {"state": True}      #初始变量
    if models.ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id):     #判断是否为同一用户点赞

        pollResponse["state"]=False
    else:
        with transaction.atomic():
            models.ArticleUpDown.objects.create(user_id=user_id,article_id=article_id)      #创建一个新的用户
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)   #给文章的点赞数+1

    return HttpResponse(json.dumps(pollResponse))



def down_count(request):
    '''点赞函数，禁止同一用户点赞多次'''
    user_id = request.user.nid  # 当前用户的ID
    article_id = request.POST.get("article_id")  # 获取到当前的文章ID

    downResponse = {"state": True}
    if models.Article.objects.filter(nid=article_id,user_id=user_id).first():     #判断是否为同一用户点赞
        downResponse["state"]=False
    else:
        with transaction.atomic():
            print("=========可以到这里")
            models.ArticleUpDown.objects.create(nid=user_id,article_id=article_id)      #创建一个新的用户
            models.Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)   #给文章的点赞数+1

    print("===============>",downResponse)

    return HttpResponse(json.dumps(downResponse))



def com(request,username):
    current_user = request.user
    article_id = request.POST.get("article_id")  # 当前的文章ID
    content = request.POST.get("text")  # 当前的评论内容
    print("===============content>",content)
    user_id = request.user.nid
    parent_comment_id = request.POST.get("parent_comment_id")
    response = {"success":False}
    print("===========>可以走到这里")
    if request.POST.get("parent_comment_id"):    #可以去到父级ID，为父级的评论
        with transaction.atomic():
            comment_obj = models.Comment.objects.create(content=content, user_id=user_id, article_id=article_id,
                                          parent_comment_id=parent_comment_id)
            response["success"] = True
            response["parent_comment_username"]=comment_obj.parent_comment.user.username
            response["parent_comment_content"]=comment_obj.parent_comment.content
            response["comment_id"] = comment_obj.nid
    else:                        #这里娶不到，为根评论
        print("===============>根评论")
        with transaction.atomic():
            comment_obj= models.Comment.objects.create(content=content, user_id=user_id, article_id=article_id)
            response["success"] = True
            response["comment_id"] = comment_obj.nid

    return HttpResponse(json.dumps(response))



def commentTree(request,article_id):
    # 找到当前文章对应的所有的评论
    comment_list = models.Comment.objects.filter(article_id=article_id).values("nid","content","parent_comment_id","user__username")
    comment_dict = {}
    for comment in comment_list:
        comment["chidren_commentList"] = []           #添加一个字段
        comment_dict[comment["nid"]] = comment        #创建一个字典，字典的键为nid，值为评论


    commentTree = []
    for comment in comment_list:
        pid = comment.get("parent_comment_id")         #获取到父级评论的iD
        if pid:
            comment_dict[pid]["chidren_commentList"].append(comment)   #吧该条记录添加到字典中 --------父级评论
        else:
            commentTree.append(comment)                   #没有获取到说明是根评论
    print("==============>",comment_dict)
    return HttpResponse(json.dumps(commentTree))             #串过去的是一个具有父子结构关系的字典








# 后台管理首页
def backIndex(request,username):
    if not request.user.is_authenticated():     #没有通过验证，直接跳转到收益也
        return redirect("/login/")

    article_obj = models.Article.objects.filter(user__username=username)
    paginator = Paginator(article_obj, 4)
    page_range = paginator.page_range
    num = request.GET.get("page", 1)
    article_obj = paginator.page(num)
    return render(request, "backendindex.html",locals())




import datetime
def addarticle(request,username):
    if request.method=="GET":
        print("=============这里是直接通过后台跳转过来的")
        article_form = ArticleForm()
        cate_list = models.Category.objects.filter(blog__user=request.user)
        tag_list = models.Tag.objects.filter(blog__user=request.user)
        return render(request,"addarticle.html",locals())
    else:
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():           #验证
            title = request.POST.get("title")
            content = request.POST.get("content")
            article_obj = models.Article.objects.create(title=title, desc=content[0:30],create_time=datetime.datetime.now(),user=request.user)
            models.ArticleDetail.objects.create(content=content,article=article_obj)
            return render(request,"addarticle.html",locals())
        return render(request,"addarticle.html",locals())


def delarticle(request,username):
    if request.method=="POST":
        response = {"is_del":False}
        article_nid = request.POST.get("article_nid")
        models.Article.objects.filter(nid=article_nid).delete()
        response["is_del"]=True
        return HttpResponse(json.dumps(response))


def editarticle(request,username):
    if request.method=="POST":

        return HttpResponse("OK")








def uploadFile(request):
    # 这里只有在串文件的时候才会显示
    file_obj = request.FILES.get("imgFile")           #获取到文件对象
    file_name = file_obj.name         #获取到文件名字
    from blogCMS import settings
    import os
    path = os.path.join(settings.MEDIA_ROOT,"article_uploads",file_name)        #文件上传的地址
    with open(path,"wb") as f:
        for i in file_obj.chunks():
            f.write(i)
    response = {
        "error":0,
        "url":"/media/article_uploads/"+file_name+"/"                   #文件的路径
    }
    import json
    return HttpResponse(json.dumps(response))









def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)




def pcajax_validate(request):
    if request.method == "POST":
        login_response = {"is_login":False,"error_msg":None}
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        # 验证用户名密码
        if result:
            username = request.POST.get("username")
            password = request.POST.get("password")
            print("==========>",username,password)
            user = auth.authenticate(username=username, password=password)
            if user:
                print("====可以到")
                login_response["is_login"] = True
                auth.login(request,user)
            else:
                login_response["error_msg"] = "用户名或密码错误"
        else:
            login_response["error_msg"] = "验证码错误"
        return HttpResponse(json.dumps(login_response))
    return HttpResponse("error")















def ajax(request):
    callbacks = request.GET.get("login")       #发起跨域方给的名字

    # print("=======func_name",callbacks)
    import json
    print("啊")
    s = {"name":"egon","age":18}
    return HttpResponse("%s('%s')" % (callbacks, json.dumps(s)))







from io import BytesIO
import random
from PIL import Image,ImageDraw,ImageFont
fonttype = ImageFont.truetype("static/font/kumo.ttf")

def check_code(width=120,height=30,char_length=5,font_file=fonttype,font_size=27):
    code = []
    img = Image.new(mode="RGB",size=(width,height),color=(255,255,255))
    draw = ImageDraw.Draw(img,mode="RGB")
    def rndChar():    #随机小写字母
        return chr(random.randint(65,90))
    def rnddChar():    #随机大写字母
        return chr(random.randint(96,122))
    def rndColor():     #随机颜色
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    font = ImageFont.truetype(font_file,font_size)
    for i in range(char_length):
        char = rndChar()
        chhar = rnddChar()
        code.append(char,chhar)
        for i in code:
            h = random.randint(0,4)
            draw.text([i*width/char_length,h],i,font=font,fill=rndColor())

    for i in range(25):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=rndColor())

    for i in range(25):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=rndColor())
        x = random.randint(0,width)
        y = random.randint(0,height)
        draw.arc((x,y,x+4,y+4),0,90,fill=rndColor())

    for i in range(6):
        x1 = random.randint(0,width)
        y1 = random.randint(0,height)
        x2 = random.randint(0,width)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=rndColor())

    return img,"".join(code)
























