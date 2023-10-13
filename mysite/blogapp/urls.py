from django.urls import path
from .views import ArticlesListView, CreateArticleView, ArticleDetailView

app_name = "blogapp"

urlpatterns = [
    path("", ArticlesListView.as_view(), name="articles_list"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_details"),
    path("create/", CreateArticleView.as_view(), name="create_article"),
]

