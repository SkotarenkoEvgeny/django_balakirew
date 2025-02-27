from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView

from women.forms import AddPostForm, UploadFileForm
from women.models import Category, Women, TagPost, UploadFile

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


class WomenHome(TemplateView):
    template_name = 'women/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.published.all().select_related('cat'),
        'cat_selected': 0,
        }

    # def get_context_data(self, **kwargs):
    #     context = super(WomenHome, self).get_context_data(**kwargs)
    #     context['menu'] = menu
    #     context['title'] = 'Главная страница'
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(file):
#     with open(f"uploads/{file.name}", 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)


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


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {'title': post.title, 'meny': menu, 'post': post, 'cat_selected': 1}
    return render(request, 'women/post.html', context=data)


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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.objects.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рублика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        }
    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('tag')

    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None
        }
    return render(request, 'women/index.html', context=data)
