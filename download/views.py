# -*- coding: utf-8 -*-
# Create your views here.

import mimetypes
import os
import sys
import uuid

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from uofm import auth

from .models import Download_File, History_Record, Platform, Software

USE_SENDFILE_ACCEL = True  # this should be a setting for the site.

if USE_SENDFILE_ACCEL and settings.DEBUG and 'runserver' in sys.argv:
    USE_SENDFILE_ACCEL = False


def get_remaining_downloads(user, software):

    if user.is_superuser or user.is_staff:
        return -1
    if software.download_limit is None:
        return -1

    records = History_Record.objects.filter(
        Active=True, user=user, software=software)
    date_list = set(records.values_list('when', flat=True))
    if len(date_list) > software.download_limit:
        return 0

    return software.download_limit - len(date_list)


@auth.uofm_only
def list_software(request):

    software_list = Software.objects.list_for_user(request.user)
    if len(software_list) == 1:

        return HttpResponseRedirect(
            reverse('download-list-platform', args=[str(software_list[0])]))

    return render(request, 'download/list_software.html', context=locals())


@auth.uofm_only
def list_platform(request, software):

    selected_software = Software.objects.get_for_user(request.user, software)
    if selected_software is None:
        raise Http404

    file_list = Download_File.objects.filter(software=selected_software)
    platform_list = list(set([file.platform for file in file_list]))

    if len(platform_list) == 1:
        return HttpResponseRedirect(
            reverse(
                'download-list-download',
                args=[software, str(platform_list[0])]))

    remaining_downloads = get_remaining_downloads(request.user,
                                                  selected_software)

    template_list = [
        'download/{0}.html'.format(software),
        'download/list_platform.html',
    ]

    return render(request, template_list, context=locals())


@auth.uofm_only
def list_download(request, software, platform):

    selected_software = Software.objects.get_for_user(request.user, software)
    if selected_software is None:
        raise Http404
    selected_platform = get_object_or_404(Platform, slug=platform)
    download_list = Download_File.objects.filter(
        software=selected_software, platform=selected_platform)

    remaining_downloads = get_remaining_downloads(request.user,
                                                  selected_software)

    template_list = [
        'download/{0}_{1}.html'.format(software, platform),
        'download/{0}.html'.format(software),
        'download/list_download.html',
    ]

    return render(request, template_list, context=locals())


@auth.uofm_only
def download_file(request, software, platform, fileslug):

    selected_software = Software.objects.get_for_user(request.user, software)
    if selected_software is None:
        raise Http404
    selected_platform = get_object_or_404(Platform, slug=platform)
    selected_download = get_object_or_404(
        Download_File,
        slug=fileslug,
        software=selected_software,
        platform=selected_platform)
    remaining_downloads = get_remaining_downloads(request.user,
                                                  selected_software)
    if remaining_downloads == 0:
        #assert False, 'no downloads remaining'
        raise Http404

    if not os.path.exists(selected_download.filename):
        #assert False, 'path does not exist!'
        raise Http404

    base_file = os.path.split(selected_download.filename)[-1]

    use_sendfile = getattr(settings, 'USE_SENDFILE_ACCEL', None)
    if use_sendfile is None:
        use_sendfile = USE_SENDFILE_ACCEL

    # mod_xsendfile
    #   Inspired by Satchmo's DownloadLink product and send_file view.
    #   http://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    #   http://bitbucket.org/chris1610/satchmo/src/48bdc3c050b3/satchmo/apps/product/modules/downloadable/views.py
    #   (as of 2010-Aug-26).
    if use_sendfile:
        file_url = selected_download.filename

        response = HttpResponse()
        # For Nginx
        response['X-Accel-Redirect'] = file_url
        # For Apache and Lighttpd v1.5
        response['X-Sendfile'] = file_url
        # For Lighttpd v1.4
        response['X-LIGHTTPD-send-file'] = file_url
        response['Content-Disposition'] = "attachment; filename=%s" % base_file
        response['Content-length'] = os.path.getsize(file_url)
    else:
        # fallback, for debugging.
        response = HttpResponse(open(selected_download.filename, 'rb'))
        response['Content-Disposition'] = 'attachment; filename=%s' % base_file
        response['Content-Length'] = str(
            os.path.getsize(selected_download.filename))

    contenttype, encoding = mimetypes.guess_type(base_file)
    if contenttype:
        response['Content-type'] = contenttype
    History_Record(user=request.user, software=selected_software).save()
    return response


#
