from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from blog.models import Post


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
