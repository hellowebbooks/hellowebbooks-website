from collections import namedtuple, OrderedDict


_ProductType = namedtuple('ProductType', ['name', 'description', 'amount', 'paperback_addl', 'us_postage', 'can_postage', 'eur_postage', 'aus_postage', 'else_postage'])

class Product(_ProductType):
    __slots__ = ()
    def __str__(self):
        return self.name

PRODUCT_LOOKUP = {
    # Hello Web Books
    'hwb-video': Product('hwb-video', 'Hello Web Books Video Package', 19900, 3000, 322, 1400, 2000, 2900, 2100, ),
    'hwb-pb': Product('hwb-pb', 'Hello Web Books Paperback Package', 7995, 0, 322, 1400, 2000, 2900, 2100, ),
    'hwb-ebooks': Product('hwb-ebooks', 'Hello Web Books eBook Package', 4995, 3000, 322, 1400, 2000, 2900, 2100, ),
    # Hello Web App
    'hwa-video': Product('hwa-video', 'Hello Web App Video Package', 17900, 2000, 322, 1000, 1500, 2000, 1800, ),
    'hwa-pb': Product('hwa-pb', 'Hello Web App Paperback Package', 5995, 0, 322, 1000, 1500, 2000, 1800, ),
    'hwa-ebooks': Product('hwa-ebooks', 'Hello Web App eBook Package', 3495, 2000, 322, 1000, 1500, 2000, 1800, ),
    'hwa-video-supplement': Product('hwa-video-supplement', 'Hello Web App Video Supplement', 14405, 2000, 322, 1000, 1500, 2000, 1800, ),
    # Hello Web Design
    'hwd-video': Product('hwd-video', 'Hello Web Design Video Package', 9900, 1000, 300, 800, 1300, 2000, 1500, ),
    'hwd-pb': Product('hwd-pb', 'Hello Web Design Paperback Package', 3995, 0, 300, 800, 1300, 2000, 1500, ),
    'hwd-ebooks': Product('hwd-ebooks', 'Hello Web Design eBook Package', 2495, 1000, 300, 800, 1300, 2000, 1500, ),
    'hwd-video-supplement': Product('hwd-video-supplement', 'Hello Web Design Video Supplement', 7405, 1000, 300, 800, 1300, 2000, 1500, ),
 }

# XXX: The content files, if they're the content from the books, need to be
# hidden from git and moved to server manually (or something)
#for key, value in hwa_course.iteritems():
#    print key, value['name']
course_list = OrderedDict({
    'Hello Web App': {
         'intro': {
            'name': 'Introduction',
            'video': 'https://vimeo.com/1',
            'template': 'course/hwa/intro.md',
         },
         'browse-page': {
            'name': 'Setting Up Basic Browse Pages',
            'video': 'https://vimeo.com/2',
            'template': 'course/hwa/browse-page.md',
         },
    },
    'Hello Web Design': {
         'intro': {
            'name': 'Introduction',
            'video': 'https://vimeo.com/1',
            'template': 'course/hwa/intro.md',
         },
         'browse-page': {
            'name': 'Setting Up Basic Browse Pages',
            'video': 'https://vimeo.com/2',
            'template': 'course/hwa/browse-page.md',
         },
    },
})
