from modeltranslation.translator import register, TranslationOptions, translator
from .models import  Blog, Category, Article



@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Category, CategoryTranslationOptions)

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = (
        'name_article',

        'min_volume',
        'font',
        'font_size',
        'line_spacing',
        'margins',
        'journal_languages',

        'header_title',
        'author_name',
        'student_info',
        'supervisor',
        'annotation',
        'key_words',
        'article_text',
        'bibliography',
        # Добавьте остальные поля модели Article здесь
    )