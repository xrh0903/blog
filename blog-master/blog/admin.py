from django.contrib import admin
from . import models
# Register your models here.
#注册每一张数据表，才会在admin页面中显示出来

admin.site.register(models.UserInfo)
admin.site.register(models.UserFans)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Comment)
admin.site.register(models.CommentUpDown)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Tag)
admin.site.register(models.Article2Tag)
admin.site.register(models.SiteArticleCategory)
admin.site.register(models.SiteCategory)


