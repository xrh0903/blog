from django.db import models
from django.contrib.auth.models import AbstractUser       #admin 表中的有些字段就不会显示

# Create your models here.


class UserInfo(AbstractUser):  # settings:   AUTH_USER_MODEL = "blog.UserInfo"
    """
    用户信息
    """
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, blank=True, null=True,  verbose_name='手机号码')
    avatar = models.FileField(verbose_name='头像', upload_to='media/avatar', default="media/avatar/default.png",null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))
    class Meta:
        verbose_name_plural = "用户信息表"

    def __str__(self):
        return self.username            #这里可以看做是验证成功返回的值


class UserFans(models.Model):
    """
    互粉关系表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')

    class Meta:
        verbose_name_plural="互粉关系表"
        unique_together = [
            ('user', 'follower'),
        ]
    def __str__(self):
        return self.user.username



class Blog(models.Model):
    """
    站点信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32,null=True,blank=True,default="/static/theme/headle.css")
    user = models.OneToOneField(to='UserInfo', to_field='nid')
    class Meta:
        verbose_name_plural = "站点信息表"
    def __str__(self):
        return self.title


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')         #一个站点多个博客
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = '博客个人分类表'
        ordering = ['title']
    def __str__(self):
        return self.title




class Article(models.Model):
    '''
    文章表，最主要的一张表
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')     #外键用更加详细的描述
    read_count = models.IntegerField(default=0,verbose_name="阅读量")
    comment_count = models.IntegerField(default=0,verbose_name="评论量")
    up_count = models.IntegerField(default=0,verbose_name="推荐")
    down_count = models.IntegerField(default=0,verbose_name="踩踩")
    create_time = models.DateTimeField(verbose_name='创建时间')       # auto_now_add    当前的时间
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)      #多个文章对应一个类型
    user = models.ForeignKey(verbose_name='所属用户', to='UserInfo', to_field='nid')              #多个文章对应一个用户
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    site_article_category = models.ForeignKey(to="SiteArticleCategory", null=True,blank=True,verbose_name="小的二级分类")


    class Meta:
        verbose_name_plural = "文章表"


    def __str__(self):
        return self.title


class SiteCategory(models.Model):
    '''
    系统分类表
    '''
    name=models.CharField(max_length=32,verbose_name="系统的分类")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "系统分类表"



class SiteArticleCategory(models.Model):
    '''
    系统文章分类表
    '''
    name=models.CharField(max_length=32,verbose_name="系统分类下的分类表")
    site_category=models.ForeignKey(to="SiteCategory",blank=True,null=True,verbose_name="所属系统分类")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "系统分类分类表表"



class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')   #每个文章的简介只是对应一片文章
    class Meta:
        verbose_name_plural = "文章详细表"
    def __str__(self):
        return self.article.title


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(default=0)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')     #评论表是由多个人组件起来的
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')         #评论的是文章
    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')     #自关联，父级评论
    class Meta:
        verbose_name_plural = "评论表"
    # def __str__(self):
    #     return self.user.username


class CommentUpDown(models.Model):
    """
    评论点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)         #用户点赞
    comment = models.ForeignKey("Comment", null=True)       #对评论点赞
    state = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "评论点赞表"
        unique_together = [('user', 'comment')]
    def __str__(self):
        return self.comment.user.username



class ArticleUpDown(models.Model):
    """
    文章点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)    #用户点赞
    article = models.ForeignKey("Article", null=True)   #文章点赞
    state = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "文章点赞表"
        unique_together = [('user', 'article')]

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    '''
    标签表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')     #多个标签属于一个博客，，
    class Meta:
        verbose_name_plural = "标签表"
    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    '''
    文章标签的第二张表，自己新建的
    '''
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')     #对应文章
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')             #对应标签
    class Meta:
        verbose_name_plural="文章标签对应表"
        unique_together = [
            ('article', 'tag'),
        ]
    def __str__(self):
        return self.article.title+"+"+self.tag.title
