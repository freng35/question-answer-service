from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import U
from django.views.generic.edit import FormView
from .forms import *


def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def tmp(request, user_id):
    t = U
    return render(request, 'tmp.html', {})


class RegisterFormView(FormView):
    form_class = SignUpForm
    # Ссылка, на которую будет перенаправляться user
    # в случае успешной регистрации
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        for key in form.fields:
            print(form.fields[key])

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)