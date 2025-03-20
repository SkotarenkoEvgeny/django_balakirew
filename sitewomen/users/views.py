from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import LoginUserForm, RegisterUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


def register(request):
    form = RegisterUserForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return render(request, 'users/register_done.html')
    return render(request, 'users/register.html', {'form': form})
