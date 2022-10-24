# from email.policy import default
# from tkinter.tix import Tree

# from cProfile import label

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

'''
Você pode encontrar mais detalhes sobre os tipos de atributos nos links abaixo..  # noqa: E501
https://django-portuguese.readthedocs.io/en/1.0/ref/models/fields.html
https://docs.djangoproject.com/pt-br/3.2/ref/models/fields/

Opões importantes do models.ForeignKey ...

    * on_delete=models.SET_NULL
        Se a chave da tabela origem for eliminada, o campo vinculado recebe NULL. Nesse caso,
        deve-se incluir também a opção (null=True) para permitir que o atributo receba Null.

    * on_delete = models.CASCADE
        Se a chave da tabela origem for eliminada, todos os registros da tabela vinculada
        que contenham a chave também serão excluídos.

    * on_delete=models.PROTECT
        Impede que o objeto (registro) seja excluído, se houver outros objetos vinculados a ele.

    * on_delete=models.RESTRICT
        Semelhante ao PROTECT, mas permite exclusão em cascata, se o objeto referenciado estiver
        como CASCADE de outro objeto.

    * existem outras opções, caso queira pesquisar: SET_DEFAULT, DO_NOTHING e SET(alguma_funcao)

'''


class Category(models.Model):
    name = models.CharField(max_length=65)

    # para permitir ver o conteúdo do registro na consulta na admin do django
    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name='Título')
    description = models.CharField(max_length=165, verbose_name='Descrição')
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name='Tempo de preparação')
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name='Unidade do tempo de preparação')
    servings = models.IntegerField(verbose_name='Porções')
    servings_unit = models.CharField(
        max_length=65, verbose_name='Unidade das porções')
    preparation_steps = models.TextField(verbose_name='Etapas de preparação')
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name='Etapas de preparação em HTML')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name='Publicado')
    # o blank permite que o campo cover fique sem string
    # default coloca string vazia por padrão no campo cover
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name='Imagem'
    )
    # linka category com a classe Category
    # se a Category for apagada, coloca null em category.
    # nesse caso, category deve permitir valores nulos.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name='Categoria')  # noqa: E501
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')

    # para permitir ver o conteúdo do registro na consulta na admin do django
    def __str__(self):
        return self.title

    # possibilita ver a recipe no site da aplicação,
    # através de botão "ver no site", na tela de admin do django
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
