from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# from registration.backends.simple.views import RegistrationView
#
# # Create a new class that redirects the user to the index page, if successful at logging
# class MyRegistrationView(RegistrationView):
#     def get_success_url(self,request, user):
#         return '/netdev/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^netdev/', include('netdev.urls')),
    # url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    # (r'^accounts/', include('registration.backends.simple.urls')),
)
