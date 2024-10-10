# type:ignore
from typing import Any
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Page
from django.db.models import Q
from django.views.generic.list import ListView
PER_PAGE = 1

class PostListView(ListView):
    model = Post
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context.update({
            'page_title': 'Home - '
        })

        return context


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
            'page_title': 'Home - '
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
            'page_title': 'Created_by - ',
        }
    )

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type:ignore
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    page_title = f'Categoria - {page_obj[0].category.name} - '
    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj, 
            'page_title': page_title,
        }
    )

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug) # type:ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    page_title = f'Tag - {page_obj[0].tags.first().name} - '

    return render(
        request,
        'pages/index.html',
        {
            'page_obj': page_obj, 
            'page_title': page_title,
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

    page_title = f'{search_value[:25]} - Search - '
    
    return render(
        request,
        'pages/index.html',
        {
            'page_obj': posts, 
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True, slug=slug).first()
    
    if page_obj is None:
        raise Http404

    page_title = f'Pagina - {page_obj.title} - '
    
    return render(
        request,
        'pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )

def post(request, slug):
    post_obj = get_object_or_404(Post, slug=slug, is_published=True)

    if post_obj is None:
        raise Http404

    page_title = f'Post - {post_obj.title} - '

    return render(
        request,
        'pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
