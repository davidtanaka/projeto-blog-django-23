# type:ignore
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.db.models import Q
PER_PAGE = 9

def index(request):
    posts = Post.objects.get_published() # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def created_by(request, author_id):
    posts = Post.objects.get_published().filter(created_by__pk=author_id) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj, 
        }
    )

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type:ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj, 
        }
    )

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug) # type:ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj, 
        }
    )

def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) | 
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
        )
    )[:PER_PAGE]
    
    return render(
        request,
        'pages/index.html',
        {
            'page_obj': posts, 
            'search_value': search_value,
        }
    )


def page(request):
    return render(
        request,
        'pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )

def post(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(
        request,
        'pages/post.html',
        {
            'post': post,
        }
    )
