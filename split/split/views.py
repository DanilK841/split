from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.http import HttpResponse, HttpRequest

def MainPageView(request: HttpRequest):
    context = {
        'products': {'1':100,},
    }
    return render(request, 'main/index.html', context=context)
