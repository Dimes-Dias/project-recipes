from email.policy import default
from tkinter.tix import Tree

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    # para permitir ver o conteúdo do registro na consulta na admin do django
    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # o blank permite que o campo cover fique sem string
    # default coloca string vazia por padrão no campo cover
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    # linka category com a classe Category
    # se a Category for apagada, coloca null em category.
    # nesse caso, category deve permitir valores nulos.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None,)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    # para permitir ver o conteúdo do registro na consulta na admin do django
    def __str__(self):
        return self.title
