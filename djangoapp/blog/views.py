# type: ignore
from typing import Any
from blog.models import Page, Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty=False
    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'Categoria - {self.object_list[0].category.name} - '
        ctx.update({
            'page_title': page_title
        })
        return ctx
        


class TagListView(PostListView):
    allow_empty=False
    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'Tag - {self.object_list[0].tags.first().name} - '
        ctx.update({
            'page_title': page_title
        })
        return ctx


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'Search - {search_value[:30]} - ',
            'search_value': search_value,
        })
        return ctx

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'Página - {page.title} - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

def page(request, slug):
    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'Post - {post.title} - '  # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
