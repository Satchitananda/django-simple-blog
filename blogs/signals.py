# coding=utf-8
from django.conf import settings
from django.core.mail import send_mass_mail
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.core.urlresolvers import reverse_lazy

from .models import BlogEntry

@receiver(post_save, sender=BlogEntry, dispatch_uid="send_messages_on_entry_created")
def on_entry_created(sender, instance, created, **kwargs):
    if created:
        # sending an email to all subscribers
        site = Site.objects.get_current()
        subscribers = instance.blog.subscribers.exclude(email__isnull=True)
        if subscribers.count() > 0:
            message = u'В блоге: %s появилась новая запись с названием <a href="http://%s%s">%s.</a>' \
                % (instance.blog.title, site.domain, reverse_lazy('entry', args=[instance.id]), instance.title)
            email_data = ((
                u'Появилась новая запись в вашей ленте',
                u'Здравствуйте %s!<br />' % s.first_name + message,
                settings.DEFAULT_FROM_EMAIL,
                [s.email]
            ) for s in subscribers)
            send_mass_mail(email_data)
