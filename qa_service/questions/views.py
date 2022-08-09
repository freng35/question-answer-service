from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


@login_required
def create_question(request):
    context = {}

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_item = Question(
                user_created=request.user,
                theme=form.data.get('theme', None),
                text=form.data.get('text', None),
            )
            question_item.save()
            return HttpResponseRedirect(f'/question/{question_item.id}')

    form = QuestionForm()
    context['form'] = form

    return render(request, 'create_question.html', context)


def get_question(request, question_id):
    if not Question.objects.filter(id=question_id).exists():
        raise Http404()

    question_item = Question.objects.get(id=question_id)
    context = {'question': question_item}
    answer_item = Answer.objects.filter(question=question_item)
    try:
        user_liked = Like.objects.get(question=question_item, user_from_like=request.user)
    except:
        user_liked = None

    if user_liked:
        context['liked'] = True
    else:
        context['liked'] = False

    context['likes_count'] = question_item.amount_of_likes()
    context['answers'] = answer_item
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_tmp_item = Answer(
                question=question_item,
                user_answered=request.user,
                text=form.data.get('text', None),
            )
            answer_tmp_item.save()
            return HttpResponseRedirect(f'/question/{question_id}')

    form = AnswerForm()
    context['form'] = form
    return render(request, 'question.html', context)


@login_required
def like(request, question_id):

    if request.method == "POST":
        question_item = Question.objects.get(id=question_id)
        try:
            like_item = Like.objects.get(
                question=question_item,
                user_from_like=request.user
            )
            like_item.delete()
        except:
            like_item = Like(
                question=question_item,
                user_from_like=request.user
            )
            like_item.save()

    return HttpResponseRedirect(f'/question/{question_id}')