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


@login_required()
def profile(request, user_id):
    context = {}
    user_item = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user_item)
    context['profile'] = user_profile
    context['c_user'] = user_item

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
            print(request.FILES)
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


def create_question(request):
    context = {}

    if request.method == "POST":
        form = CreateQuestionFrom(request.POST)
        if form.is_valid():
            question_item = Question(
                user_created=request.user,
                theme=form.data.get('theme', None),
                text=form.data.get('text', None),
            )
            question_item.save()
            return HttpResponseRedirect(f'/question/{question_item.id}')

    form = CreateQuestionFrom()
    context['form'] = form

    return render(request, 'create_question.html', context)


def get_question(request, question_id):
    question_item = Question.objects.get(id=question_id)
    context = {'question': question_item}

    return render(request, 'question.html', context)

