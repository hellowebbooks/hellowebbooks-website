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

#for key, value in hwa_course.iteritems():
#    print key, value['name']
course_list = OrderedDict({
    'Hello Web App': {
        'Hello Web App': {
            '0': {
                'name': 'Hello Web App Introduction',
                'video': '',
                'template': 'course/hwa/intro.md',
                'link': 'intro',
            },
            '1': {
                'name': "What We’re Building",
                'video': '',
                'template': 'course/hwa/what-building.md',
                'link': 'what-building',
            },
            '2': {
                'name': 'Prerequisites',
                'video': '',
                'template': 'course/hwa/prerequisites.md',
                'link': 'prerequisites',
            },
            '3': {
                'name': 'Getting Started',
                'video': 'https://player.vimeo.com/video/322468325',
                'template': 'course/hwa/getting-started.md',
                'link': 'getting-started',
            },
            '4': {
                'name': 'Setting up your Templates',
                'video': 'https://player.vimeo.com/video/125105042',
                'template': 'course/hwa/setting-templates.md',
                'link': 'setting-templates',
            },
            '5': {
                'name': 'Fun with Template Tags',
                'video': 'https://player.vimeo.com/video/125107452',
                'template': 'course/hwa/template-tags.md',
                'link': 'template-tags',
            },
            '6': {
                'name': 'Adding Dynamic Data',
                'video': 'https://player.vimeo.com/video/125112251',
                'template': 'course/hwa/dynamic-data.md',
                'link': 'dynamic-data',
            },
            '7': {
                'name': 'Displaying Dynamic Information in the Templates',
                'video': 'https://player.vimeo.com/video/125113570',
                'template': 'course/hwa/dynamic-templates.md',
                'link': 'dynamic-templates',
            },
            '8': {
                'name': 'Setting up Individual Object Pages',
                'video': 'https://player.vimeo.com/video/125114336',
                'template': 'course/hwa/indiv-object-pages.md',
                'link': 'indiv-object-pages',
            },
            '9': {
                'name': 'Forms.py Funsies',
                'video': 'https://player.vimeo.com/video/125116321',
                'template': 'course/hwa/forms.md',
                'link': 'forms',
            },
            '10': {
                'name': 'Adding a Registration Page',
                'video': 'https://player.vimeo.com/video/125118325',
                'template': 'course/hwa/reg-page.md',
                'link': 'reg-page',
            },
            '11': {
                'name': 'Associating Users with Objects',
                'video': 'https://player.vimeo.com/video/322475015',
                'template': 'course/hwa/user-objects.md',
                'link': 'user-objects',
            },
            '12': {
                'name': 'Setting up Basic Browse Pages',
                'video': 'https://player.vimeo.com/video/125185864',
                'template': 'course/hwa/browse-page.md',
                'link': 'browse-page',
            },
            '13': {
                'name': 'Quick Hits: 404 Pages, requirements.txt, and Testing',
                'video': 'https://player.vimeo.com/video/125195379',
                'template': 'course/hwa/quick-hits.md',
                'link': 'quick-hits',
            },
            '14': {
                'name': 'Deploying Your Web App',
                'video': 'https://player.vimeo.com/video/125203626',
                'template': 'course/hwa/deploying.md',
                'link': 'deploying',
            },
            '15': {
                'name': 'What To Do If Your App is Broken',
                'video': '',
                'template': 'course/hwa/broken.md',
                'link': 'broken',
            },
            '16': {
                'name': 'Important Things to Know',
                'video': '',
                'template': 'course/hwa/important-know.md',
                'link': 'important-know',
            },
            '17': {
                'name': 'Moving Forward',
                'video': '',
                'template': 'course/hwa/moving-forward.md',
                'link': 'moving-forward',
            },
            '18': {
                'name': 'Special Thanks',
                'video': '',
                'template': 'course/hwa/special-thanks.md',
                'link': 'special-thanks',
            },
        },
        'Video Extras': {
            '0': {
                'name': 'Example: Real Life Code',
                'video': 'https://player.vimeo.com/video/124584929',
                'template': 'course/empty.md',
                'link': 'real-life-code',
            },
            '1': {
                'name': 'Example: Adding A New Feature',
                'video': 'https://player.vimeo.com/video/124593641',
                'template': 'course/empty.md',
                'link': 'extra-new-feature',
            },
            '2': {
                'name': 'Example: Using Git',
                'video': 'https://player.vimeo.com/video/124581543',
                'template': 'course/empty.md',
                'link': 'using-git',
            },
            '3': {
                'name': 'Example: Using the Command Line',
                'video': 'https://player.vimeo.com/video/124364480',
                'template': 'course/empty.md',
                'link': 'using-command-line',
            },
        },
        'Intermediate Concepts': {
            '0': {
                'name': 'Intermediate Concepts Introduction',
                'video': '',
                'template': 'course/hwaic/introduction.md',
                'link': 'introduction',
            },
            '1': {
                'name': 'Creating a Contact Form and Working with Custom Forms',
                'video': 'https://player.vimeo.com/video/147784115',
                'template': 'course/hwaic/contact-form.md',
                'link': 'contact-form',
            },
            '2': {
                'name': 'Adding a New Model',
                'video': 'https://player.vimeo.com/video/147789199',
                'template': 'course/hwaic/new-model.md',
                'link': 'new-model',
            },
            '3': {
                'name': 'Adding Easy Admin Emails, Helpers, Sitemaps, and More',
                'video': 'https://player.vimeo.com/video/147789913',
                'template': 'course/hwaic/misc.md',
                'link': 'misc',
            },
            '4': {
                'name': 'Adding User-Uploaded Images',
                'video': 'https://player.vimeo.com/video/147791632',
                'template': 'course/hwaic/user-uploaded-images.md',
                'link': 'user-uploaded-images',
            },
            '5': {
                'name': 'Editing and Resizing Images',
                'video': 'https://player.vimeo.com/video/147868862',
                'template': 'course/hwaic/resizing-images.md',
                'link': 'resizing-images',
            },
            '6': {
                'name': 'Setting Up Django Messages for Alerts',
                'video': 'https://player.vimeo.com/video/148555627',
                'template': 'course/hwaic/django-messages.md',
                'link': 'django-messages',
            },
            '7': {
                'name': 'Front-End Fun: Adding Gulp, Sass, and Bootstrap',
                'video': 'https://player.vimeo.com/video/148565556',
                'template': 'course/hwaic/sass-bootstrap.md',
                'link': 'sass-bootstrap',
            },
            '8': {
                'name': 'Reading Source Code And Setting Up a Form to Edit User Email Addresses',
                'video': 'https://player.vimeo.com/video/148569412',
                'template': 'course/hwaic/reading-source.md',
                'link': 'reading-source',
            },
            '9': {
                'name': 'Adding Payments with Stripe',
                'video': 'https://player.vimeo.com/video/148574316',
                'template': 'course/hwaic/stripe.md',
                'link': 'stripe',
            },
            '10': {
                'name': 'Adding an API',
                'video': 'https://player.vimeo.com/video/150557037',
                'template': 'course/hwaic/api.md',
                'link': 'api',
            },
            '11': {
                'name': 'Working with Sessions',
                'video': 'https://player.vimeo.com/video/150557885',
                'template': 'course/hwaic/sessions.md',
                'link': 'sessions',
            },
            '12': {
                'name': 'Creating Your Own Scripts and a Bit About Cron Jobs',
                'video': 'https://player.vimeo.com/video/150558862',
                'template': 'course/hwaic/cronjobs.md',
                'link': 'cronjobs',
            },
            '12': {
                'name': 'Database Pitfalls',
                'video': 'https://player.vimeo.com/video/150559647',
                'template': 'course/hwaic/database-pitfalls.md',
                'link': 'database-pitfalls',
            },
            '13': {
                'name': 'Resources',
                'video': '',
                'template': 'course/hwaic/resources.md',
                'link': 'resources',
            },
            '14': {
                'name': 'Thanks',
                'video': '',
                'template': 'course/hwaic/thanks.md',
                'link': 'thanks',
            },
        },
    },
    'Hello Web Design': {
        'Module 1': {
            '0.00': {
                'name': 'Foreword',
                'video': '',
                'template': 'course/hwd/foreword.md',
                'link': 'foreword',
            },
            '0.0': {
                'name': 'Introduction',
                'video': 'https://player.vimeo.com/video/322480097',
                'template': 'course/hwd/intro.md',
                'link': 'intro',
            },
            '1.0': {
                'name': 'If You Only Read One Chapter, Make It This One',
                'video': 'https://player.vimeo.com/video/322480267',
                'template': 'course/hwd/one-chapter.md',
                'link': 'one-chapter',
            },
        },
        'Module 2': {
            '2.0': {
                'name': 'Theory and Design Principles',
                'video': '',
                'template': 'course/hwd/theory.md',
                'link': 'theory',

            },
            '2.1': {
                'name': 'Grid',
                'video': 'https://player.vimeo.com/video/322480426',
                'template': 'course/hwd/grid.md',
                'link': 'grid',
            },
            '2.2': {
                'name': 'Color',
                'video': 'https://player.vimeo.com/video/322480564',
                'template': 'course/hwd/color.md',
                'link': 'color',
            },
            '2.3': {
                'name': 'Typography',
                'video': 'https://player.vimeo.com/video/322480679',
                'template': 'course/hwd/typography.md',
                'link': 'typography',
            },
            '2.4': {
                'name': 'White Space',
                'video': 'https://player.vimeo.com/video/322480801',
                'template': 'course/hwd/white-space.md',
                'link': 'white-space',
            },
            '2.5': {
                'name': 'Layout and Hierarchy',
                'video': 'https://player.vimeo.com/video/322480937',
                'template': 'course/hwd/layout.md',
                'link': 'layout',
            },
            '2.6': {
                'name': 'Content',
                'video': 'https://player.vimeo.com/video/322481048',
                'template': 'course/hwd/content.md',
                'link': 'content',
            },
            '2.7': {
                'name': 'User Experience',
                'video': 'https://player.vimeo.com/video/322481441',
                'template': 'course/hwd/ux.md',
                'link': 'ux',
            },
            '2.8': {
                'name': 'Images and Imagery',
                'video': 'https://player.vimeo.com/video/322481555',
                'template': 'course/hwd/images.md',
                'link': 'images',
            },
            '2.9': {
                'name': 'Extra Tidbits',
                'video': 'https://player.vimeo.com/video/322481739',
                'template': 'course/hwd/tidbits.md',
                'link': 'tidbits',
            },
        },
        'Module 3': {
            '3.0': {
                'name': 'The Process and Training Your Design Eye',
                'video': '',
                'template': 'course/hwd/process.md',
                'link': 'process',
            },
            '3.1': {
                'name': 'Finding Inspiration',
                'video': 'https://player.vimeo.com/video/322481899',
                'template': 'course/hwd/inspiration.md',
                'link': 'inspiration',
            },
            '3.2': {
                'name': 'Planning',
                'video': 'https://player.vimeo.com/video/322482078',
                'template': 'course/hwd/planning.md',
                'link': 'planning',
            },
            '3.3': {
                'name': 'Prototypes',
                'video': 'https://player.vimeo.com/video/324816425',
                'template': 'course/hwd/prototypes.md',
                'link': 'prototypes',
            },
            '3.4': {
                'name': 'Getting Feedback',
                'video': 'https://player.vimeo.com/video/322482231',
                'template': 'course/hwd/feedback.md',
                'link': 'feedback',
            },
            '3.5': {
                'name': 'Coding Your Design',
                'video': 'https://player.vimeo.com/video/324816579',
                'template': 'course/hwd/coding.md',
                'link': 'coding',
            },
        },
        'Module 4': {
            '4.0': {
                'name': 'Reassurances',
                'video': 'https://player.vimeo.com/video/324816712',
                'template': 'course/hwd/reassurances.md',
                'link': 'reassurances',
            },
            '5.0': {
                'name': 'Additional Resources',
                'video': '',
                'template': 'course/hwd/additional-resources.md',
                'link': 'additional-resources',
            },
            '5.1': {
                'name': 'Final Thoughts',
                'video': '',
                'template': 'course/hwd/final-thoughts.md',
                'link': 'final-thoughts',
            },
            '5.2': {
                'name': 'Special Thanks',
                'video': '',
                'template': 'course/hwd/special-thanks.md',
                'link': 'special-thanks',
            },
            '5.3': {
                'name': 'About Author',
                'video': '',
                'template': 'course/hwd/about-author.md',
                'link': 'about-author',
            },
        },
    },
    'Really Friendly Command Line Intro': {
        'Zine': {
            '0': {
                'name': 'Introduction',
                'video': 'https://player.vimeo.com/video/328691402',
                'template': 'course/cmd/intro.md',
                'link': 'intro',
            },
            '1': {
                'name': 'Let’s start playing!',
                'video': '',
                'template': 'course/cmd/playing.md',
                'link': 'playing',
            },
            '2': {
                'name': 'But I’m tired of typing already!',
                'video': '',
                'template': 'course/cmd/tired.md',
                'link': 'tired',
            },
            '3': {
                'name': 'Intermediate command line utilities',
                'video': '',
                'template': 'course/cmd/intermediate.md',
                'link': 'intermediate',
            },
            '4': {
                'name': 'Wait, something went wrong',
                'video': '',
                'template': 'course/cmd/wrong.md',
                'link': 'wrong',
            },
            '5': {
                'name': 'Conclusion',
                'video': '',
                'template': 'course/cmd/conclusion.md',
                'link': 'conclusion',
            },
        },
    },
    'Really Friendly Git Intro': {
        'Zine': {
            '0': {
                'name': 'Introduction',
                'video': '',
                'template': 'course/git/intro.md',
                'link': 'intro',
            },
            '1': {
                'name': 'What is Git?',
                'video': '',
                'template': 'course/git/whatsgit.md',
                'link': 'whatsgit',
            },
            '2': {
                'name': 'Let’s start playing!',
                'video': '',
                'template': 'course/git/playing.md',
                'link': 'playing',
            },
            '3': {
                'name': 'Intermediate Git: Creating branches!',
                'video': '',
                'template': 'course/git/intermediate.md',
                'link': 'intermediate',
            },
            '4': {
                'name': 'That’s cool! So what’s GitHub then?',
                'video': '',
                'template': 'course/git/github.md',
                'link': 'github',
            },
            '5': {
                'name': 'Conclusion',
                'video': '',
                'template': 'course/git/conclusion.md',
                'link': 'conclusion',
            },
        },
    },
})
