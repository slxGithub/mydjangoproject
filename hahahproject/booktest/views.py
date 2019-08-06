from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, request
from .models import BookInfo
from django.http import Http404


# Create your views here.


def index(request):
    book_list = BookInfo.objects.order_by('bpub_date')[:5]
    context = {'title':'hahha','book_list': book_list}
    return render(request, 'booktest/index.html', context)


def detail(request,book_id):
    try:
        book_info = BookInfo.objects.get(id=book_id)
    except Exception as e:
        raise Http404('not found')
    return render(request,'booktest/detail.html',{'book_info':book_info})
