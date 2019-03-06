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
        'Hello Web App': {
            '0': {
                'name': 'Hello Web App Introduction',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/intro.md',
                'link': 'intro',
            },
            '1': {
                'name': "What We’re Building",
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/what-building.md',
                'link': 'what-building',
            },
            '2': {
                'name': 'Prerequisites',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/prerequisites.md',
                'link': 'prerequisites',
            },
            '3': {
                'name': 'Getting Started',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/getting-started.md',
                'link': 'getting-started',
            },
            '4': {
                'name': 'Setting up your Templates',
                'video': 'https://player.vimeo.com/video/147791632',
                'template': 'course/hwa/setting-templates.md',
                'link': 'setting-templates',
            },
            '5': {
                'name': 'Fun with Template Tags',
                'video': 'https://player.vimeo.com/video/150559647',
                'template': 'course/hwa/template-tags.md',
                'link': 'template-tags',
            },
            '6': {
                'name': 'Adding Dynamic Data',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/dynamic-data.md',
                'link': 'dynamic-data',
            },
            '7': {
                'name': 'Displaying Dynamic Information in the Templates',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/dynamic-templates.md',
                'link': 'dynamic-templates',
            },
            '8': {
                'name': 'Setting up Individual Object Pages',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/indiv-object-pages.md',
                'link': 'indiv-object-pages',
            },
            '9': {
                'name': 'Forms.py Funsies',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/forms.md',
                'link': 'forms',
            },
            '10': {
                'name': 'Adding a Registration Page',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/reg-page.md',
                'link': 'reg-page',
            },
            '11': {
                'name': 'Associating Users with Objects',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/user-objects.md',
                'link': 'user-objects',
            },
            '12': {
                'name': 'Setting up Basic Browse Pages',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwa/browse-page.md',
                'link': 'browse-page',
            },
            '13': {
                'name': 'Quick Hits: 404 Pages, requirements.txt, and Testing',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/quick-hits.md',
                'link': 'quick-hits',
            },
            '14': {
                'name': 'Deploying Your Web App',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/deploying.md',
                'link': 'deploying',
            },
            '15': {
                'name': 'What To Do If Your App is Broken',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/broken.md',
                'link': 'broken',
            },
            '16': {
                'name': 'Important Things to Know',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwa/important-know.md',
                'link': 'important-know',
            },
            # TODO: Add pages without a video here?
        },
        'Intermediate Concepts': {
            '0': {
                'name': 'Intermediate Concepts Introduction',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/introduction.md',
                'link': 'introduction',
            },
            '1': {
                'name': 'Creating a Contact Form and Working with Custom Forms',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/contact-form.md',
                'link': 'contact-form',
            },
            '2': {
                'name': 'Adding a New Model',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/new-model.md',
                'link': 'new-model',
            },
            '3': {
                'name': 'Adding Easy Admin Emails, Helpers, Sitemaps, and More',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/misc.md',
                'link': 'misc',
            },
            '4': {
                'name': 'Adding User-Uploaded Images',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/user-uploaded-images.md',
                'link': 'user-uploaded-images',
            },
            '5': {
                'name': 'Editing and Resizing Images',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/resizing-images.md',
                'link': 'resizing-images',
            },
            '6': {
                'name': 'Setting Up Django Messages for Alerts',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/django-messages.md',
                'link': 'django-messages',
            },
            '7': {
                'name': 'Front-End Fun: Adding Gulp, Sass, and Bootstrap',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/sass-bootstrap.md',
                'link': 'sass-bootstrap',
            },
            '8': {
                'name': 'Reading Source Code And Setting Up a Form to Edit User Email Addresses',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/reading-source.md',
                'link': 'reading-source',
            },
            '9': {
                'name': 'Adding Payments with Stripe',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/stripe.md',
                'link': 'stripe',
            },
            '10': {
                'name': 'Adding an API',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/api.md',
                'link': 'api',
            },
            '11': {
                'name': 'Working with Sessions',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/sessions.md',
                'link': 'sessions',
            },
            '12': {
                'name': 'Creating Your Own Scripts and a Bit About Cron Jobs',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/cronjobs.md',
                'link': 'cronjobs',
            },
            '12': {
                'name': 'Database Pitfalls',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwaic/database-pitfalls.md',
                'link': 'database-pitfalls',
            },
            # TODO: Add pages without a video here?
        },
    },
    'Hello Web Design': {
        'Module 1': {
            '0.0': {
                'name': 'Introduction',
                'video': 'https://vimeo.com/1',
                'template': 'course/hwd/intro.md',
                'link': 'intro',
            },
            '1.0': {
                'name': 'If You Only Read One Chapter, Make It This One',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/one-chapter.md',
                'link': 'one-chapter',
            },
        },
        'Module 2': {
            '2.0': {
                'name': 'Theory and Design Principles',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/theory.md',
                'link': 'theory',

            },
            '2.1': {
                'name': 'Grid',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/grid.md',
                'link': 'grid',
            },
            '2.2': {
                'name': 'Color',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/color.md',
                'link': 'color',
            },
            '2.3': {
                'name': 'Typography',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/typography.md',
                'link': 'typography',
            },
            '2.4': {
                'name': 'White Space',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/white-space.md',
                'link': 'white-space',
            },
            '2.5': {
                'name': 'Layout and Hierarchy',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/layout.md',
                'link': 'layout',
            },
            '2.6': {
                'name': 'Content',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/content.md',
                'link': 'content',
            },
            '2.7': {
                'name': 'User Experience',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/ux.md',
                'link': 'ux',
            },
            '2.8': {
                'name': 'Images and Imagery',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/images.md',
                'link': 'images',
            },
            '2.9': {
                'name': 'Extra Tidbits',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/tidbits.md',
                'link': 'tidbits',
            },
        },
        'Module 3': {
            '3.0': {
                'name': 'The Process and Training Your Design Eye',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/process.md',
                'link': 'process',
            },
            '3.1': {
                'name': 'Finding Inspiration',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/inspiration.md',
                'link': 'inspiration',
            },
            '3.2': {
                'name': 'Planning',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/planning.md',
                'link': 'planning',
            },
            '3.3': {
                'name': 'Prototypes',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/prototypes.md',
                'link': 'prototypes',
            },
            '3.4': {
                'name': 'Getting Feedback',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/feedback.md',
                'link': 'feedback',
            },
            '3.5': {
                'name': 'Coding Your Design',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/coding.md',
                'link': 'coding',
            },
        },
        'Module 4': {
            '4.0': {
                'name': 'Reassurances',
                'video': 'https://vimeo.com/2',
                'template': 'course/hwd/reassurances.md',
                'link': 'reassurances',
            },
        },
        # TODO: Add pages without a video here?
    },
})
