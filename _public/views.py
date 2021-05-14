from django.shortcuts import render
from _db import models


def index_view(request):
    return render(request, 'public/index.html',
                  context={
                      'page': models.WebsiteMainPage.get_solo(),
                      'page_blocks': models.WebsiteMainPageBlocks.objects.all(),
                      'contact': models.WebsiteContacts.get_solo(),
                  })


def about_view(request):
    return render(request, 'public/about.html',
                  context={
                      'page': models.WebsiteAbout.get_solo(),
                      'page_blocks': models.WebsiteAboutGallery.objects.all(),
                  })


def services_view(request):
    return render(request, 'public/services.html',
                  context={
                      'page': models.WebsiteService.get_solo(),
                      'page_blocks': models.WebsiteServiceBlocks.objects.all(),
                  })


def contact_view(request):
    return render(request, 'public/contact.html',
                  context={
                      'page': models.WebsiteContacts.get_solo(),
                  })


def error_view(request):
    return render(request, 'public/error.html')