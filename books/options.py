from collections import namedtuple


_ProductType = namedtuple('ProductType', ['name', 'description', 'amount', ])

class Product(_ProductType):
    __slots__ = ()
    def __str__(self):
        return self.name

PRODUCT_LOOKUP = {
    'hwb-video': Product('hwb-video', 'Hello Web Books Video Package', 19900,),
    'hwb-pb': Product('hwb-pb', 'Hello Web Books Paperback Package', 7995,),
    'hwb-ebooks': Product('hwb-ebooks', 'Hello Web Books eBook Package', 4995,),
    'hwa-video': Product('hwa-video', 'Hello Web App Video Package', 17900,),
    'hwa-pb': Product('hwa-pb', 'Hello Web App Paperback Package', 5995,),
    'hwa-ebooks': Product('hwa-ebooks', 'Hello Web App eBook Package', 3495,),
    'hwd-video': Product('hwd-video', 'Hello Web Design Video Package', 9900,),
    'hwd-pb': Product('hwd-pb', 'Hello Web Design Paperback Package', 3995,),
    'hwd-ebooks': Product('hwd-ebooks', 'Hello Web Design eBook Package', 2495,),
 }
