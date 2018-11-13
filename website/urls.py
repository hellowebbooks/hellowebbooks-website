from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from books import views


urlpatterns = [
    # website pages
    path('', views.index, name='index'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('donate/', TemplateView.as_view(template_name='donate.html'), name='donate'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('migrate/', TemplateView.as_view(template_name='migrate.html'), name='migrate'),
    path('order/', TemplateView.as_view(template_name='order.html'), name='order'),
    path('press/', TemplateView.as_view(template_name='press.html'), name='press'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy-policy.html'), name='privacy-policy'),
    path('samples/', TemplateView.as_view(template_name='samples.html'), name='samples'),
    path('setup/', TemplateView.as_view(template_name='setup.html'), name='setup'),
    path('start/', TemplateView.as_view(template_name='start.html'), name='start'),
    path('unsubscribe/', TemplateView.as_view(template_name='unsubscribe.html'), name='unsubscribe'),
    path('workshops/', TemplateView.as_view(template_name='workshops.html'), name='workshops'),
    path('write/', TemplateView.as_view(template_name='write.html'), name='write'),

    # books and courses
    path('django-intermediate-concepts/', TemplateView.as_view(template_name='django-intermediate-concepts.html'), name='django-intermediate-concepts'),
    path('learn-command-line/', TemplateView.as_view(template_name='learn-command-line.html'), name='learn-command-line'),
    path('learn-design/', TemplateView.as_view(template_name='learn-design.html'), name='learn-design'),
    path('learn-django/', TemplateView.as_view(template_name='learn-django.html'), name='learn-django'),

    # blog
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('news/', include(wagtail_urls)),

    # admin
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
