from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    phones_objects = Phone.objects.all()


    if sort == 'name':
        phones_objects = phones_objects.order_by('name')
    elif sort == 'min_price':
        phones_objects = phones_objects.order_by('price')
    elif sort == 'max_price':
        phones_objects = phones_objects.order_by('price').reverse()


    context = {'phones': phones_objects}
    return render(request, template, context=context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context=context)
