from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView, RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.contrib.auth.views import password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from books import views
from books.sitemap import StaticSitemap, HomepageSitemap, PostPageSitemap

sitemaps = {
    #'things': ThingSitemap,
    'static': StaticSitemap,
    'homepage': HomepageSitemap,
    'postpage': PostPageSitemap,
}

urlpatterns = [
    # website pages
    path('', views.index, name='index'),
    path('order/', views.order, name='order'),

    # static pages
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('donate/', TemplateView.as_view(template_name='donate.html'), name='donate'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('gitignore/', TemplateView.as_view(template_name='gitignore.html'), name='gitignore'),
    path('migrate/', TemplateView.as_view(template_name='migrate.html'), name='migrate'),
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

    # dashboard and logged in views
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/edit-email/', views.edit_email, name="edit_email"),
    path('dashboard/hello-web-app/', views.hwa, name="hwa"),
    path('dashboard/hello-web-design/', views.hwd, name="hwd"),
    path('dashboard/<product_id>/', views.product_page, name="product_page"),

    # payment views
    path('charge/update/', views.charge_update, name="charge_update"),
    path('charge/<product>/', views.charge, name='charge'),
    #path('charge/cancel/', views.charge_cancel, name="charge_cancel"),
    path('buy/<product>/', views.upsell, name='upsell'),
    path('gift/<product>/', views.gift, name='gift'),
    path('check_coupon/', views.check_coupon, name='check_coupon'),

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
    path('accounts/password/change/', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    path('accounts/password/change/done/', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),

    path('login/', RedirectView.as_view(url='/accounts/login/')),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('accounts/', include('registration.backends.simple.urls')),

    # redirects
    path('web-design/', RedirectView.as_view(pattern_name='learn-design', permanent=True)),
    path('original/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('intermediate-concepts/', RedirectView.as_view(pattern_name='django-intermediate-concepts', permanent=True)),
    path('preorder/', RedirectView.as_view(pattern_name='order', permanent=True)),
    path('cmd-line-pdf/', RedirectView.as_view(url='https://goo.gl/LLGswY')),
    path('cmd-line-printable/', RedirectView.as_view(url='https://goo.gl/B38FeX')),

    path('category/casestudy/', RedirectView.as_view(url='/news/category/casestudy/')),
    path('category/tutorial/', RedirectView.as_view(url='/news/category/tutorial/')),
    path('category/interviews/', RedirectView.as_view(url='/news/category/interviews/')),
    path('category/production/', RedirectView.as_view(url='/news/category/production/')),
    path('category/design/', RedirectView.as_view(url='/news/category/design/')),
    path('category/development/', RedirectView.as_view(url='/news/category/development/')),

    path('tutorial/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/about-author/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/broken/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/browse-page/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/deploying/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/dynamic-data/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/dynamic-templates/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/forms/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/friendly-note/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/getting-started/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/important-know/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/indiv-object-pages/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/intro/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/moving-forward/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/prerequisites/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/quick-hits/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/references/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/reg-page/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/setting-templates/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/special-thanks/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/template-tags/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/user-objects/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),
    path('tutorial/what-building/', RedirectView.as_view(pattern_name='learn-django', permanent=True)),

    # admin
    #path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
