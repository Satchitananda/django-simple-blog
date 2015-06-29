# coding=utf-8
from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, FormView, CreateView, DetailView

from .models import Blog, BlogEntry, AlreadyReadEntry
from .forms import LoginForm


auth_required = login_required(login_url=reverse_lazy('login'))

class PageTitleMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PageTitleMixin, self).get_context_data(**kwargs)
        context.update({
            'page_title': getattr(self, 'page_title', '')
        })
        return context


class FeedView(PageTitleMixin, ListView):
    template_name = 'feed.html'
    page_title = u'Лента'
    context_object_name = 'feed'

    @method_decorator(auth_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FeedView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        read_entries_ids = list(AlreadyReadEntry.objects.filter(user=self.request.user).values_list('entry_id', flat=True))
        return BlogEntry.objects\
            .filter(blog_id__in=list(self.request.user.subscriptions.values_list('id', flat=True)))\
            .exclude(id__in=read_entries_ids).order_by('-created')


class LoginView(PageTitleMixin, FormView):
    form_class = LoginForm
    template_name = 'login.html'
    page_title = u'Войти'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.execute(self.request)
        return super(LoginView, self).form_valid(form)

class CreatePostView(PageTitleMixin, CreateView):
    model = BlogEntry
    fields = ['title', 'text']
    page_title = u'Создать запись'
    template_name = 'create.html'
    success_url = reverse_lazy('create')

    @method_decorator(auth_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePostView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.blog = self.request.user.blog
        entry.save()
        messages.success(self.request, u'Запись успешно создана')
        return super(CreatePostView, self).form_valid(form)


class MarkAsReadView(View):
    @method_decorator(auth_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MarkAsReadView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        mark_as_read = request.POST.get('mark_as_read', 'true') in ['true', '1']
        entry_id = request.POST.get('id')
        if mark_as_read:
            AlreadyReadEntry.objects.get_or_create(user=self.request.user, entry_id=entry_id)
            return HttpResponse('ok')
        else:
            AlreadyReadEntry.objects.filter(entry_id=entry_id).delete()
            return HttpResponse('ok')


class EntryView(PageTitleMixin, DetailView):
    template_name = 'entry.html'
    model = BlogEntry
    page_title = u'Запись'
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super(EntryView, self).get_context_data(**kwargs)
        context.update({
            'already_read': list(AlreadyReadEntry.objects
                                 .filter(user=self.request.user)
                                 .values_list('entry_id', flat=True))
        })
        return context


class BlogListView(PageTitleMixin, ListView):
    queryset = User.objects.select_related('blog')
    template_name = 'blog_list.html'
    page_title = u'Список блогов'
    context_object_name = 'users'

    @method_decorator(auth_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BlogListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context.update({
            'user_subscription_ids': list(self.request.user.subscriptions
                .select_related()
                .values_list('author__blog__id', flat=True)),
        })
        return context

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get('blog_id')
        subscribe = request.POST.get('subscribe', 'true') in ['true', '1']
        blog = Blog.objects.get(id=blog_id)

        if subscribe:
            blog.subscribers.add(self.request.user)
        else:
            blog.subscribers.remove(self.request.user)
        return HttpResponse('ok')
