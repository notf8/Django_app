from django.urls import reverse_lazy
from .models import Article
from django.views.generic import ListView, CreateView, DetailView


class ArticlesListView(ListView):
    template_name = "blogapp/articles-list.html"
    context_object_name = "articles"
    queryset = (
        Article.objects
        .select_related("author", "category")
        .prefetch_related("tags")
    )


class ArticleDetailView(DetailView):
    queryset = (
        Article.objects
        .select_related("author")
        .prefetch_related("tags")
    )


class CreateArticleView(CreateView):
    model = Article
    fields = "title", "content", "author", "category", "tags",
    success_url = reverse_lazy("blogapp:articles_list")

