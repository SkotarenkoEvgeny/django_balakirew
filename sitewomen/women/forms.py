from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label='Категория не выбрана',
                                 label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(),
                                     empty_label='Не замужем',
                                     required=False, label='Муж')
    class Meta:
       model = Women
       fields = ['title', 'slug', 'photo', 'content', 'is_published', 'cat', 'husband', 'tags']
       widgets = {
           'title': forms.TextInput(attrs={'class': 'form-input'}),
           'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
       }
       labels = {"slug": "URL"}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(required=False, label='E-mail',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
