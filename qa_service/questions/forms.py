from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['theme'].label = 'Тема'
        self.fields['text'].label = 'Вопрос'
        self.fields['text'].widget = forms.Textarea(attrs={'style': 'width: 90%;'})

    class Meta:
        model = Question
        fields = ('theme', 'text')


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        self.fields['text'].label = 'Ответ'
        self.fields['text'].widget = forms.Textarea(attrs={'style': 'width: 75%;'})

    class Meta:
        model = Question
        fields = ('text', )