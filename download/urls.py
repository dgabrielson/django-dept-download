from django.conf.urls import url

from . import views

#
#  Add the following to your site urls.py to activate.
#
#    (r'^download/', include('download.urls')),
#

# https://www.stats.umanitoba.ca/download/jmp/windows
# https://www.stats.umanitoba.ca/download/jmp/mac

#Basic premise:
#https://www.stats.umanitoba.ca/download/
#- prompts for user credentials, authenticates, etc.
#- presents users with a list of available downloads, if not specified
#https://www.stats.umanitoba.ca/download/<software>/
#- presents users with a list of available platforms, if there is more than one
#https://www.stats.umanitoba.ca/download/<software>/<platform>/
#- downloads the software package for the indicated platform

urlpatterns = [
    url(
        r'^(?P<software>[\w-]+)/(?P<platform>[\w-]+)/(?P<fileslug>[\w-]+)/$',
        views.download_file,
        name='download-download-file',
    ),
    url(
        r'^(?P<software>[\w-]+)/(?P<platform>[\w-]+)/$',
        views.list_download,
        name='download-list-download',
    ),
    url(
        r'^(?P<software>[\w-]+)/$',
        views.list_platform,
        name='download-list-platform',
    ),
    url(
        r'^$',
        views.list_software,
        name='download-main',
    ),
]
