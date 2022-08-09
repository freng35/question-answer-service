from django.urls import path

import questions.views as view

urlpatterns = [
    path('create_question/', view.create_question),
    path('question/<int:question_id>/', view.get_question),
    path('question/<int:question_id>/like/', view.like),
]