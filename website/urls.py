from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, reverse_lazy
from django.views.generic import TemplateView, RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from blog.feeds import PostFeed
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
    path('start/', RedirectView.as_view(url='/accounts/login/')),
    path('unsubscribe/', TemplateView.as_view(template_name='unsubscribe.html'), name='unsubscribe'),
    path('keepme/', TemplateView.as_view(template_name='keepme.html'), name='keepme'),
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

    # course and video pages
    path('course/<product_slug>/', views.course, name="course"),
    path('course/<product_slug>/<link>/', views.course, name="course_link"),
    path('course/', RedirectView.as_view(pattern_name='dashboard')),

    # payment views
    path('charge/update/', views.charge_update, name="charge_update"),
    path('charge/<product_slug>/', views.charge, name='charge'),
    #path('charge/cancel/', views.charge_cancel, name="charge_cancel"),
    path('buy/<product_slug>/', views.upsell, name='upsell'),
    path('gift/<product_slug>/', views.gift, name='gift'),
    path('check_coupon/', views.check_coupon, name='check_coupon'),

    # registration
    path('accounts/password/reset/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.txt',
        ),
        name='password_reset'),
    path('accounts/password/reset/done/',
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('accounts/password/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            post_reset_login=True,
        ),
        name='password_reset_confirm'),
    path('accounts/password/giftee/<uidb64>/<token>/',
        views.GifteePasswordResetConfirmView.as_view(),
        name="giftee_password_reset_confirm"),
    path('accounts/password/done/',
        PasswordResetDoneView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('accounts/password/change/',
        PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
        name='password_change'),
    path('accounts/password/change/done/',
        PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
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

    # blog categories redirects
    path('category/casestudy/', RedirectView.as_view(url='/news/category/casestudy/')),
    path('category/tutorial/', RedirectView.as_view(url='/news/category/tutorial/')),
    path('category/interviews/', RedirectView.as_view(url='/news/category/interviews/')),
    path('category/production/', RedirectView.as_view(url='/news/category/production/')),
    path('category/design/', RedirectView.as_view(url='/news/category/design/')),
    path('category/development/', RedirectView.as_view(url='/news/category/development/')),

    # old tutorial redirects
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
    path('admin/dashboard/add-customer-bulk/', views.admin_add_customer_bulk, name='admin_add_customer_bulk'),
    path('admin/dashboard/add-customer/', views.admin_add_customer, name='admin_add_customer'),
    path('admin/dashboard/export-emails/', views.admin_export_customer_emails, name='admin_export_customer_emails'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),

    # rss
    path('rss.xml', PostFeed(), name='rss-feed'),
    path('rss/', PostFeed(), name='rss-feed'),

    # sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
