from django.contrib import admin
from .models import Blog, Category, MultipleImage, Article
from modeltranslation.admin import TranslationAdmin
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin.widgets import AdminFileWidget


class MultipleImageInlineForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminFileWidget)
    delete_image = forms.BooleanField(required=False)

    class Meta:
        model = MultipleImage
        fields = ['image', 'delete_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['image'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        if 'delete_image' in cleaned_data and cleaned_data['delete_image']:
            cleaned_data['image'].delete()
        return cleaned_data
class MultipleImageInline(admin.TabularInline):
    model = MultipleImage
    form = MultipleImageInlineForm
    extra = 1

    def image_preview(self, obj):
        return mark_safe('<img src="{}" style="max-height: 200px; max-width: 200px"/>'.format(obj.image.url))

    image_preview.short_description = 'IMAGE PREVIEW'

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj=obj))
        if obj:
            fields.remove('delete_image')
        return fields

    fields = ('image_preview', 'image', 'delete_image')
    readonly_fields = ('image_preview',)


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ("title_ru", "title_uz", "title_en", "user","approved")
    inlines = [MultipleImageInline]


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = ("name", "name_uz", "name_en")

admin.site.register(MultipleImage)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ("name_article_ru", "name_article_uz", "name_article_en")