from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'password')


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password_2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_2')
        labels = {'email': 'E-mail', 'first_name': 'Имя', 'last_name': 'Фамилия'}

    def clean_password_2(self):
        password = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_2')
        if password != password_2:
            raise forms.ValidationError('Пароли не совпадают')
        return password_2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f'email - {email} is already registered')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(this_year-100, this_year-5)))

    class Meta:
        model = get_user_model()
        fields = ('photo', 'username', 'email', 'date_birth', 'first_name', 'last_name')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия'}
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-input'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-input'})}


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
