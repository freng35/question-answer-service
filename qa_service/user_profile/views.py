from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import *
from .models import *
from questions.models import *


def profile(request, user_id):
    context = {}
    if not User.objects.filter(id=user_id).exists():
        raise Http404()

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
    if not User.objects.filter(id=user_id).exists():
        raise Http404()

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
