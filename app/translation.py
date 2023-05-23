from modeltranslation.translator import register, TranslationOptions, translator
from .models import  Blog, Category 



@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Category, CategoryTranslationOptions)