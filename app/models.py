from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Blog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500, verbose_name='Название')
    description = RichTextField('Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', verbose_name='Пользователь', null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='blogs', verbose_name='Категория', null=True)
    file = models.FileField(upload_to='files/', blank=True, verbose_name='Файл для скачивания(pdf)')
    views_count = models.PositiveIntegerField(default=0)
    approved = models.BooleanField(default=False, verbose_name='Подтверждено')

    def __str__(self):
        return f'{self.title} ===> {self.user}'

    def increment_views(self):
        self.views_count += 1
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
class MultipleImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images', verbose_name='Блог')
    image = models.ImageField(upload_to='blog_photos/', verbose_name='Изображение')
    delete_image = models.BooleanField(default=False)

    def __str__(self):
        return self.blog.title
    

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'




class Article(models.Model):

    name_article = models.CharField(max_length=255, verbose_name='Требования к оформлению статьи...(в научном...    )')


    min_volume = models.CharField(max_length=255, verbose_name='Минимальный объем статьи', blank=True, null=True)
    font = models.CharField(max_length=255, verbose_name='Шрифт', blank=True, null=True)
    font_size = models.CharField(max_length=255, verbose_name='Размер шрифта', blank=True, null=True)
    line_spacing = models.CharField(max_length=255,  verbose_name='Междустрочный интервал', blank=True, null=True)
    margins = models.CharField(max_length=255, verbose_name='Поля', blank=True, null=True)
    journal_languages = models.CharField(max_length=255, verbose_name='Языки журнала', blank=True, null=True)
    # Другие поля модели

    

    header_title = models.TextField(blank=True, null=True, verbose_name='Заголовок/название статьи', max_length=255)
    author_name = models.TextField(blank=True, null=True, verbose_name='ФИО автора', max_length=255)
    student_info = models.TextField(blank=True, null=True, verbose_name=' Ученое звание, Студент, магистрант или аспирант, вуз, страна, город', max_length=255)
    supervisor = models.TextField(blank=True, null=True, verbose_name='Научный руководитель', max_length=255)
    annotation = models.TextField(blank=True, null=True, verbose_name='Аннотация', max_length=255)
    key_words = models.TextField(blank=True, null=True, verbose_name='Ключевые слова', max_length=255)
    article_text = models.TextField(blank=True, null=True, verbose_name='Текст статьи/Текст статьи на английском языке', max_length=255)
    bibliography = models.TextField(blank=True, null=True, verbose_name='Список литературы/Список литературы на английском языке', max_length=255)


    instruction = models.FileField(upload_to='reqs/', blank=True, verbose_name='Инструкция оформления')
    # Другие поля модели

    class Meta:
        verbose_name = 'Требование статьи'
        verbose_name_plural = 'Требования статей'
