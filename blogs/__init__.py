default_app_config = 'blogs.BlogsAppConfig'

from django.apps import AppConfig

class BlogsAppConfig(AppConfig):
    name = 'blogs'

    def ready(self):
        from blogs import signals
