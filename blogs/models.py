# coding=utf-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.fields.related import SingleRelatedObjectDescriptor


# from django-annoying
class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    """
    The descriptor that handles the object creation for an AutoOneToOneField.
    """
    def __get__(self, instance, instance_type=None):
        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return (super(AutoSingleRelatedObjectDescriptor, self)
                    .__get__(instance, instance_type))
        except model.DoesNotExist:
            obj = model(**{self.related.field.name: instance})

            obj.save()

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return (super(AutoSingleRelatedObjectDescriptor, self)
                    .__get__(instance, instance_type))


class AutoOneToOneField(models.OneToOneField):
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))


class Blog(models.Model):
    author = AutoOneToOneField(User, verbose_name=u'автор')
    subscribers = models.ManyToManyField(User, verbose_name=u'подписчики', related_name='subscriptions')

    @property
    def title(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'блог пользователя'
        verbose_name_plural = u'блоги пользователей'

    def __unicode__(self):
        return u'Блог им. %s' % (self.author.get_full_name() or u'%(username)')


class BlogEntry(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=u'блог')
    title = models.CharField(u'заголовок', max_length=255)
    text = models.TextField(u'текст записи')
    created = models.DateTimeField(u'создана')
    updated = models.DateTimeField(u'обновлена')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(BlogEntry, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'запись'
        verbose_name_plural = u'записи'

    def __unicode__(self):
        return self.title


class AlreadyReadEntry(models.Model):
    user = models.ForeignKey(User, verbose_name=u'подписчик')
    entry_id = models.IntegerField(u'ID записи')

    class Meta:
        verbose_name = u'прочитанная запись'
        verbose_name_plural = u'прочитанные записи'

    def __unicode__(self):
        return self.entry_id
