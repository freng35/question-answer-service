from django.shortcuts import render
from simple_search import search_filter
from .forms import *
from questions.models import *


def index(request):
    question_item = Question.objects.all()
    form = SearchForm()
    res = {}

    if request.method == "POST":
        form = SearchForm(request.POST)
        search_fields = ['theme', 'text']
        questions = [Question.objects.filter(search_filter(search_fields, form.data['text']))]
    else:
        for item in question_item:
            likes = item.amount_of_likes()
            try:
                res[likes].append(item)
            except KeyError:
                res[likes] = [item]

        i = 0
        questions = []
        for key in sorted(res.keys(), reverse=True):
            if i < 5:
                questions.append(res[key])
            else:
                break

    context = {
        'questions': questions,
        'form': form
    }

    return render(request, 'index.html', context)
