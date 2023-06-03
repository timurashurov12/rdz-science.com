from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Category, MultipleImage, Article
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, ArticleForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from modeltranslation import settings as mt_settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse



def download_file(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, str(post.file))
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def download_instruction(request, pk):
    model_instance = get_object_or_404(Article, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, str(model_instance.instruction))
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def home(request):
    requirements = Article.objects.all()
    popular_blogs = Blog.objects.filter(approved=True).order_by('-views_count')[:4]
    context = {
        'popular_blogs': popular_blogs,
        'reqs': requirements
    }
    return render(request, 'home.html', context)





def about_article(request, id):
    req = get_object_or_404(Article, id=id)
    context = {
        'req': req
    }
    return render(request, 'about_article.html', context)


def blogs_view(request, category_slug=None):
    categories = Category.objects.all()
    latest_blogs = Blog.objects.filter(approved=True).order_by('-created_at')[:3]
    blogs = Blog.objects.filter(approved=True).order_by('-created_at')
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        blogs = blogs.filter(category=category)
    p = Paginator(blogs, 8, orphans=0)
    page = request.GET.get('page')
    pages = p.get_page(page)
    nums = pages.paginator.get_elided_page_range(number=pages.number, on_each_side=2, on_ends=1)
    context = {
        'latest_blogs': latest_blogs,
        'nums': nums,
        'pages': pages,
        'categories': categories,
        'current_category_slug': category_slug,
        'category': category
    }
    return render(request, 'blog.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    viewed_posts = request.session.get('viewed_posts', [])
    if post.pk not in viewed_posts:
        post.increment_views()
        viewed_posts.append(post.pk)
        request.session['viewed_posts'] = viewed_posts

    context = {
        'post': post
    }
    return render(request, 'blog_detail.html', context)

@login_required
def user_view(request, username, category_slug=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    categories = Category.objects.all()
    category = None #
    
    articles = Blog.objects.filter(user=user).order_by('-created_at')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)
    p = Paginator(articles, 8, orphans=0)
    page = request.GET.get('page')
    pages = p.get_page(page)
    nums = pages.paginator.get_elided_page_range(number=pages.number, on_each_side=2, on_ends=1)
    context = {
        'user': user,
        'articles': pages,
        'nums': nums,
        'categories': categories,
        'current_category_slug': category_slug, # добавляем текущий слаг категории
        'category': category 
    }
    return render(request, 'user.html', context)

def search_result(request):
    query = request.GET.get('search')
    if query:
        current_language = mt_settings.DEFAULT_LANGUAGE
        blogs = Blog.objects.filter(approved=True).filter(
            Q(**{'title_%s__icontains' % current_language: query}) |
            Q(**{'description_%s__icontains' % current_language: query})
        ).order_by('-created_at')

        p = Paginator(blogs, 6, orphans=0, allow_empty_first_page=True)
        page = request.GET.get('page')
        pages = p.get_page(page)
        nums = pages.paginator.get_elided_page_range(number=pages.number, on_each_side=2, on_ends=1)
    else:
        blogs = Blog.objects.filter(approved=True)
        pages = None
        nums = None
    categories = Category.objects.all()
    latest_blogs = Blog.objects.filter(approved=True).order_by('-created_at')[:3]

    context = {
        'blogs': blogs,
        'query': query,
        'categories': categories,
        'pages': pages,
        'nums': nums,
        'latest_blogs': latest_blogs
    }

    return render(request, 'search_result.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, '')
            return redirect('home')
        else:
            messages.error(request, '')
    else:
        form = SignUpForm()
    return render(request, 'register.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            error_message = 'Неправильно введен логин или пароль!'
            context = {'error_message': error_message}
            return render(request, 'login.html', context=context)
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Изменения сохранены!'))
            return redirect('user', username=form.cleaned_data['username'])
        else:
            messages.error(request, '')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

@login_required
def change_password(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the user's session to reflect the new password
            update_session_auth_hash(request, user)
            messages.success(request, _('Ваш пароль был успешно изменен!'))
            return redirect('user', username=username)
        else:
            messages.error(request, '')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.approved = False  # Set approved to False
            blog.save()

            # get the list of image files
            images = request.FILES.getlist('images')

            # loop through the images and create MultipleImage instances for each
            for image in images:
                MultipleImage.objects.create(blog=blog, image=image)

            messages.success(request, _('Ваш пост успешно добавлен и ожидает проверку администратора!'))
            return redirect(reverse('user', args=[request.user.username]))
        else:
            messages.error(request, '')
    else:
        form = ArticleForm()
    blogs = Blog.objects.order_by('-created_at')
    context = {
        'form': form,
        'pages': blogs,
    }
    return render(request, 'add_post.html', context)

    
@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            # удаляем изображения
            for image in blog.images.all():
                if str(image.id) in form.cleaned_data.get('delete_images', []):
                    image.delete()
                else:
                    image.delete_image = True
                    image.save()

            # сохраняем изображения
            images = request.FILES.getlist('images')
            for img in images:
                MultipleImage.objects.create(blog=blog, image=img)

            # сохраняем изменения в блоге
            form.save()
            messages.success(request, _('Пост успешно был изменен!'))
            return redirect('blog_detail', pk=blog.pk)
        else:
            if blog.images.count() == 1 and 'images' not in request.FILES and 'delete_images' not in form.cleaned_data:
                form.add_error(None, _('Необходимо добавить фотографию или удалить существующую.'))

    else:
        form = ArticleForm(instance=blog)

    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'change_blog.html', context)


@login_required
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Blog.objects.get(id=pk)
        user = delete_it.user  # получаем пользователя, который создал запись
        delete_it.delete()
        messages.success(request, _('Запись была удалена!'))
        return redirect('user', username=user.username)
    else:
        messages.success(request, '')
        return redirect('home')