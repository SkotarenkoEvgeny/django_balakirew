from tkinter import Listbox

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from women.forms import AddPostForm, UploadFileForm
from women.models import Category, Women, TagPost, UploadFile

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


class WomenHome(ListView):
    template_name = 'women/index.html'
    # model = Women
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
        }

    def get_queryset(self):
        return Women.published.all().select_related('cat')



def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFile(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                  context={'title': 'О сайте', 'menu': menu, 'form': form})


class ShowPost(DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset = None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(View):

    def get(self, request):
        form = AddPostForm()
        data = {'title': 'Добавление статьи', 'meny': menu, 'form': form}
        return render(request, 'women/add_page.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {'title': 'Добавление статьи', 'meny': menu, 'form': form}
        return render(request, 'women/add_page.html', context=data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['menu'] = menu
        context['title'] = 'Категория - ' + cat.name
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowTagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = f"Тег: {tag.tag}"
        context['cat_selected'] = None
        return context
