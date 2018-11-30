"""blogCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blogCMS import settings
from django.views.static import serve

from blog import views
from blog import urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^log_out/', views.log_out),
    url(r'^reg/', views.reg),
    url(r'^get_validCode_img/',views.get_validCode_img),

    url(r'^index/?(.*)',views.index),
    url(r'^$',views.index),
    url(r'^article/',views.article),
    url(r'^comment/',views.comment),
    url(r'^cate/(?P<site_article_category>.*)/$', views.index),

    # media配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^uploadFile/$',views.uploadFile),

    #个人站点配置
    url(r'^blog/',include("blog.urls")),
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate', views.pcajax_validate, name='pcajax_validate'),



    url(r'^ajax/',views.ajax),

]
