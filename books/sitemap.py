import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import PostPage


class PostPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return PostPage.objects.all()

    def lastmod(self, obj):
        return obj.latest_revision_created_at


class StaticSitemap(Sitemap):
    lastmod = None
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ['about', 'contact', 'courses', 'donate', 'faq', 'migrate', 'order', 'press', 'privacy-policy', 'setup', 'start', 'workshops', 'write', 'django-intermediate-concepts', 'learn-command-line', 'learn-django', 'learn-design',]

    def location(self, item):
        return reverse(item)

class HomepageSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ['index',]

    def lastmod(self, obj):
        return datetime.date.today()

    def location(self, item):
        return reverse(item)
