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
