# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BbsContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=36, verbose_name='\u6807\u9898')),
                ('smarty', models.CharField(max_length=256, verbose_name='\u7b80\u4ecb')),
                ('image', models.ImageField(default=b'static/upload/head/xy.jpg', upload_to=b'static/upload/content/', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('contents', DjangoUeditor.models.UEditorField(verbose_name='\u63cf\u8ff0', blank=True)),
                ('view_count', models.IntegerField(default=0, verbose_name='\u67e5\u770b\u6b21\u6570')),
                ('rank', models.IntegerField(default=0, verbose_name='\u8d5e')),
                ('sex_old', models.CharField(default=b'kids', max_length=5, verbose_name=b'\xe5\xb9\xb4\xe9\xbe\x84\xe7\xb1\xbb\xe5\x88\xab', choices=[(b'man', b'\xe7\x94\xb7'), (b'woman', b'\xe5\xa5\xb3'), (b'kids', b'\xe5\xb0\x8f\xe5\xad\xa9')])),
                ('top', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe7\xbd\xae\xe9\xa6\x96\xe9\xa1\xb5')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2015, 3, 30, 16, 48, 18, 776000), verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u5185\u5bb9',
                'verbose_name_plural': '\u5185\u5bb9\u7ba1\u7406\u4e2d\u5fc3',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BbsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'static/upload/head/xy.jpg', upload_to=b'static/upload/head/', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('bbs_rank', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('user', models.OneToOneField(verbose_name='\u7528\u6237\u540d', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237\u7ba1\u7406\u4e2d\u5fc3',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BbsUserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_datetime', models.DateTimeField(verbose_name='\u56de\u590d\u65f6\u95f4')),
                ('answer_content', DjangoUeditor.models.UEditorField(default=b'test', verbose_name='\u5185\u5bb9', blank=True)),
                ('answer_bbs', models.ForeignKey(verbose_name='\u6807\u9898', to='BBS.BbsContent')),
                ('answer_user', models.ForeignKey(verbose_name='\u7528\u6237\u540d', blank=True, to='BBS.BbsUser', null=True)),
            ],
            options={
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba\u7ba1\u7406\u4e2d\u5fc3',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=26, verbose_name='\u7c7b\u522b')),
            ],
            options={
                'verbose_name': '\u7c7b\u522b',
                'verbose_name_plural': '\u7c7b\u522b\u7ba1\u7406\u4e2d\u5fc3',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bbscontent',
            name='author',
            field=models.ForeignKey(verbose_name='\u53d1\u5e03\u8005', to='BBS.BbsUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bbscontent',
            name='category',
            field=models.ForeignKey(verbose_name='\u7c7b\u522b', to='BBS.Category'),
            preserve_default=True,
        ),
    ]
