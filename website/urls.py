from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView, RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

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

    # dashboard
    path('dashboard/', views.dashboard, name="dashboard"),

    # registration
    path('accounts/password/reset/', password_reset,
        {'template_name': 'registration/password_reset_form.html'}, name="password_reset"),
    path('accounts/password/reset/done/', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'}, name="password_reset_done"),
    path('accounts/password/reset/<uidb64>/<token>/', password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'}, name="password_reset_confirm"),
    path('accounts/password/done/', password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'},
        name="password_reset_complete"),
    path('accounts/', include('registration.backends.simple.urls')),

    # redirects
    path('web-design/', RedirectView.as_view(pattern_name='learn-design', permanent=True)),
    path('original/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('intermediate-concepts/', RedirectView.as_view(pattern_name='django-intermediate-concepts', permanent=True)),
    path('preorder/', RedirectView.as_view(pattern_name='order', permanent=True)),
    path('cmd-line-pdf/', RedirectView.as_view(url='https://goo.gl/LLGswY')),
    path('cmd-line-printable/', RedirectView.as_view(url='https://goo.gl/B38FeX')),

    # admin
    #path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
