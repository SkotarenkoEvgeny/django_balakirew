from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'password')
