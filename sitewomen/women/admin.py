from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Семейный стаус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return[
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
            ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']
    list_display = ('id', 'title', 'post_photo',  'time_create', 'is_published')
    list_display_links = ('id', 'title')
    readonly_fields = ('post_photo',)
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    search_fields = ('title', 'cat__name')
    list_filter = (MarriedFilter, 'is_published', 'cat__name')
    save_on_top = True


    @admin.display(description='Фото', ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width='50'>")
        return 'without photo'

    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей.")

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Снято {count} записей.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
