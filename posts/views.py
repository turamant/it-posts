from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Post, Category

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.models import User, Group


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()


def view_post_list(request, id=None):
    sort_by = request.GET.get('sort_by', 'date')
    category = None

    # Получаем категории
    categories = Category.objects.all()

    # Фильтрация по категории
    if id:
        category = get_object_or_404(Category, id=id)
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all()

    # Сортировка постов
    if sort_by == 'date':
        posts = posts.order_by('-created_at')
    elif sort_by == 'category':
        posts = posts.order_by('category__title')

    # Пагинация
    paginator = Paginator(posts, 5)  # Показывать 5 постов на странице
    page_number = request.GET.get('page', 1)  # По умолчанию первая страница, если не указано
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    print(f'Посты на текущей странице: {page_obj.object_list.count()}')
    
    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'sort_by': sort_by,
        'category': category,
        'is_authenticated': request.user.is_authenticated,
        'is_superuser': request.user.is_superuser,
    })


@login_required
def view_post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', {'post': post})
    
@login_required()
@staff_member_required()   
def view_create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

@login_required()
@staff_member_required
def view_update_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:detail', post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_update.html', {'form': form})
            

@login_required()
@staff_member_required()
def view_delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')
    
    return render(request, 'posts/post_delete.html')
    
    
