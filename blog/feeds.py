from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from blog.models import PostPage


class PostFeed(Feed):
    title = 'Hello Web Books RSS Feed'
    link = '/news/'
    description = 'News, articles, and tutorials from Hello Web Books'

    def items(self):
        return PostPage.objects.all()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
