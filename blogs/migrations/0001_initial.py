# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import blogs.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlreadyReadEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_id', models.IntegerField(verbose_name='ID \u0437\u0430\u043f\u0438\u0441\u0438')),
                ('user', models.ForeignKey(verbose_name='\u043f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043d\u0430\u044f \u0437\u0430\u043f\u0438\u0441\u044c',
                'verbose_name_plural': '\u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', blogs.models.AutoOneToOneField(verbose_name='\u0430\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(related_name='subscriptions', verbose_name='\u043f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a\u0438', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0431\u043b\u043e\u0433 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0431\u043b\u043e\u0433\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0442\u0435\u043a\u0441\u0442 \u0437\u0430\u043f\u0438\u0441\u0438')),
                ('created', models.DateTimeField(verbose_name='\u0441\u043e\u0437\u0434\u0430\u043d\u0430')),
                ('updated', models.DateTimeField(verbose_name='\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0430')),
                ('blog', models.ForeignKey(verbose_name='\u0431\u043b\u043e\u0433', to='blogs.Blog')),
            ],
            options={
                'verbose_name': '\u0437\u0430\u043f\u0438\u0441\u044c',
                'verbose_name_plural': '\u0437\u0430\u043f\u0438\u0441\u0438',
            },
        ),
    ]
