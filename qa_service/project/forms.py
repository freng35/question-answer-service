from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Profile, Question


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError("Email is already in use!")


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Profile
        fields = ('biography', 'image')


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
