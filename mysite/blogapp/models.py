from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Модель представляет Автора создаваемых статей.

    """
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    name = models.CharField(max_length=100, verbose_name="name")
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Name: {self.name!r}"


class Category(models.Model):
    """
    Модель представляет категории блога.
    Для первичного создания категорий перейдите в терминал и выполните команду 'python manage.py create_category'.
    """
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=40, verbose_name="name")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель представляет тэги для блога.
    Для первичного создания тэгов перейдите в терминал и выполните команду 'python manage.py create_tags'.
    """
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=20, verbose_name="name")

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Модель представляет статью для блога.
    """
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    title = models.CharField(max_length=200, verbose_name="title")
    content = models.TextField(max_length=500, blank=True, verbose_name="content")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="pub_date")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="category")
    tags = models.ManyToManyField(Tag, related_name="articles", verbose_name="tags")
