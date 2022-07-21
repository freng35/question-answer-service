from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import *
from .models import *


def index(request):
    context = {}
    return render(request, 'index.html', context)


def profile(request, user_id):
    context = {}
    user_item = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user_item)
    context['profile'] = user_profile
    context['c_user'] = user_item
    context['choice'] = 1  # Инфо
    if 'questions' in request.path_info:
        context['questions'] = Question.objects.filter(user_created=User.objects.get(id=user_id))
        context['choice'] = 2  # Вопросы
    if 'answers' in request.path_info:
        context['answers'] = Answer.objects.filter(user_answered=User.objects.get(id=user_id))
        context['choice'] = 3  # Ответы

    return render(request, 'profile.html', context)


@login_required()
@transaction.atomic()
def edit_profile(request, user_id):
    context = {}
    user_item = User.objects.get(id=user_id)
    context['c_user'] = user_item

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=Profile.objects.get(user=user_item))
        if form.data.get('biography') == '' and form.data.get('image') == '':
            return HttpResponseRedirect(f'/profile/{user_id}')

        if form.is_valid():
            if form.data.get('biography') != '':
                form.save()
            form.save()
            return HttpResponseRedirect(f'/profile/{user_id}')

    form = ProfileUpdateForm()
    context['form'] = form

    return render(request, 'edit_profile.html', context)


class RegisterFormView(FormView):
    form_class = SignUpForm
    success_url = "/login/"

    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        for key in form.fields:
            print(form.fields[key])

        return super(RegisterFormView, self).form_valid(form)


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

    context['likes_count'] = len(Like.objects.filter(question=question_item))
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
