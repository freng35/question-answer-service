from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import U


def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def tmp(request):
    t = U
    return render(request, 'tmp.html', {})

