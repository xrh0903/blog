# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': '文章表'},
        ),
        migrations.AlterModelOptions(
            name='articledetail',
            options={'verbose_name_plural': '文章详细表'},
        ),
        migrations.AlterModelOptions(
            name='articleup',
            options={'verbose_name_plural': '文章点赞表'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name_plural': '站点信息表'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'category', 'verbose_name_plural': '博主个人分类表'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': '评论表'},
        ),
        migrations.AlterModelOptions(
            name='commentup',
            options={'verbose_name_plural': '评论点赞表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签表'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '用户信息表'},
        ),
    ]
