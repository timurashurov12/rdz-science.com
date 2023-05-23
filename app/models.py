from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500, verbose_name='Название')
    description = models.TextField('Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', verbose_name='Пользователь', null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='blogs', verbose_name='Категория', null=True)
    file = models.FileField(upload_to='files/', blank=True, verbose_name='Файл для скачивания(pdf)')
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
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