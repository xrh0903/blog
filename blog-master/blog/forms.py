from django import forms
from django.forms import Form,fields,widgets
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError

class LoginForm(Form):
    username = fields.CharField(
        required=True,
        label='username',
        max_length=100,
        min_length=5,
        error_messages={
            "required":"用户名不能为空",
            "label":"label标签绑定出错",
            "max_length":"最大长度超过100",
            "min_length":"用户名小于5位",
        },
    widget=widgets.TextInput(attrs={"placeholder":"请输入用户名","class":"form-control"})#设置属性
     )

    password = fields.CharField(
        required=True,
        label='password',
        max_length=100,
        min_length=5,
        error_messages={
            "required":"用户名不能为空",
            "label": "label标签绑定出错",
            "max_length": "最大长度超过100",
            "min_length": "用户名小于5位",
        },
    widget=widgets.PasswordInput(attrs={"placeholder":"请输入密码","class":"form-control"}))





class RegForm(Form):

    username = fields.CharField(
        required=True,
        label='username',
        max_length=12,
        error_messages={"required":"用户名不能为空","label":"label标签绑定出错","max_length":"最大长度超过100"},
        widget=widgets.TextInput(attrs={"placeholder": "请输入用户名","id":"username","class":"form-control"})  # 设置属性
    )
    password = fields.CharField(
        required=True,
        min_length=5,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码最小长度为6', 'max_length': '密码最大长度为12', 'invalid': '密码格式错误'},
        widget=widgets.PasswordInput(attrs={"placeholder": "请输入密码","id":"password","class":"form-control"})
    )
    repassword = fields.CharField(
        required=True,
        min_length=5,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码最小长度为6', 'max_length': '密码最大长度为12', 'invalid': '密码格式错误'},
        widget=widgets.PasswordInput(attrs={"placeholder": "请再次确认密码", "id": "password", "class": "form-control"})
    )


    valid_code = fields.CharField(
        error_messages={"required": "必填"},
        widget=widgets.TextInput(attrs={"class": "form-control item", "placeholder": "验证码"})
    )
    email = fields.EmailField(
        error_messages={"required": "该字段不能为空"},
        widget=widgets.EmailInput(attrs={"class": "form-control item", "placeholder": "email"})
    )

    def clean(self):
        print("===12134567654====>",self.cleaned_data.get("password"),self.cleaned_data.get("repassword"))
        if self.cleaned_data.get("password")==self.cleaned_data.get("repassword"):
            print("===密码验证通过===")
            return self.cleaned_data
        else:
            print("===两次密码不一致")
            raise ValidationError("两次密码输入不一致")

    def clean_password(self):
        # 这里验证密码的长度
        if len(str(self.cleaned_data['password']))>8:
            print("===密码长度验证通过")
            return self.cleaned_data['password']
        else:
            print("==密码长度验证不通过")
            raise ValidationError("密码长度应该大于八位")

    def clean_valid_code(self):
        # 这里的作用是校验验证码的一致性
        if self.cleaned_data["valid_code"].upper()==self.request.session["keepValidCode"].upper():
            print("=====验证码通过===》")
            return self.cleaned_data["valid_code"]
        else:
            print("===验证码不通过")
            raise ValidationError("验证码输入错误")
    def __init__(self,request,*args,**kwargs):
        print(args,'--------init------------>')
        super(RegForm,self).__init__(*args,**kwargs)
        self.request=request

    class CommentForm(Form):
        comment_content = fields.CharField(label="",widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))


















    # avatar = fields.ImageField(
    #     # widget=widgets.FileInput(attrs={"id":"avatar","style":"background-image:url(../static/default.png)"}))
    #     # widget=widgets.FileInput(attrs={"id":"avatar","style":"width:168px;height:185px","src":"../static/default.png"}))
    #     # widget=widgets.FileInput(attrs={"id":"avatar","style":"background-image:url(../static/default.png); width:168px; height:185px;"}))
    #     widget=widgets.TextInput(attrs={"id":"avatar","class":"imgg","style":"cursor:pointer;background-image:url(../static/img/default.png); width:168px; height:185px;"}))



    # avatar = fields.ImageField(
    #
    #     widget=widgets.FileInput(attrs={"id":"avatar"})
    # )
    # create_time = fields.DateTimeField(
    #     widget=widgets.DateTimeInput(attrs={"placeholder": "请选择创建时间","id":"create_time"})
    # )













from blog.plugins import xss_plugin
class ArticleForm(Form):
    title = forms.CharField(required=True,max_length=20,error_messages={
        "required":"不能为空",
    },widget=widgets.TextInput(attrs={"placeholder": "请输入标题","class":"form-control","id":"title"}))
    content = forms.CharField(required=True,error_messages={
        "required":"不能为空",
    },widget=widgets.Textarea(attrs={
        "id":"editor_id",
    }))

    # def clean_content(self):
    #     html_str = self.cleaned_data.get("content")
    #     clean_content = xss_plugin(html_str)
    #     self.cleaned_data["content"]=clean_content
    #     return self.cleaned_data.get("content")

























