from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
# Create your views here.
def index(request):

    images = Image.objects.all()

    tag = request.GET.get('tag')
    if tag:
        images = images.filter(tags__name=tag)

    # Sortowanie obrazków po dacie publikacji
    order_by = request.GET.get('order_by')
    if order_by == 'oldest':
        images = images.order_by('data_publikacji')
    else:
        images = images.order_by('-data_publikacji')  # domyślnie sortujemy malejąco
    # Paginacja
    paginator = Paginator(images, 1)
    page_number = request.GET.get('page')
    try:
        images_page = paginator.page(page_number)
    except PageNotAnInteger:
        images_page = paginator.page(1)
    except EmptyPage:
        images_page = paginator.page(paginator.num_pages)

    context = {
        'images': images_page,
        'tag': tag,
        'order_by' : order_by,
    }
    return render(request, 'stronaglownaobrazoowa/index.html', context)

def stronaobrazka(request, Image_id):
    template = loader.get_template("stronaglownaobrazoowa/szczegolowyplik.html")
    obrazek = Image.objects.get(pk=Image_id)

    context = {
        'obrazek': obrazek,
    }
    return HttpResponse(template.render(context, request))