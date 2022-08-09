from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'style': 'width: 100%;'
                                                                                                 'height: 40px;'}),
                           label='')
