"""blog_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blogs import views

urlpatterns = [
    url(r'^$', views.FeedView.as_view(), name='feed'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^create/$', views.CreatePostView.as_view(), name='create'),
    url(r'^mark-as-read/$', views.MarkAsReadView.as_view(), name='mark_as_read'),
    url(r'^entry/(?P<pk>\d+)/$', views.EntryView.as_view(), name='entry'),
    url(r'^blog-list/$', views.BlogListView.as_view(), name='blog_list'),
]
