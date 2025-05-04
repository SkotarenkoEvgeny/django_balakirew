from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from sitewomen.settings import DEFAULT_USER_IMAGE
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm



# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

# def register(request):
#     form = RegisterUserForm(request.POST or None)
#     a = form.is_valid()
#
#     if request.POST and form.is_valid():
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()
#         # return render(request, 'users/register_done.html')
#         return reverse_lazy('users:login')
#     return render(request, 'users/register.html', {'form': form})


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя',
                     'default_image': DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
