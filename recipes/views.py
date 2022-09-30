# from http.client import HTTPResponse

from django.db.models import Q  # para usar OR (ou) no lugar de AND no filter
from django.http import Http404
from django.shortcuts import get_object_or_404, render  # , get_list_or_404
from utils.pagination import make_pagination

from recipes.models import Recipe

# from utils.recipes.factory import make_recipe

PER_PAGES = 9


def home(request):
    # recipes = Recipe.objects.all().order_by('-id')
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    # para enviar mensagens ao template...
    # from django.contrib import messages
    # exemplo de mensagens, cujas tags css estão
    # embutidas no settings.py
    # messages.success(request, 'Sua pesquisa foi efetuada.')
    # messages.error(request, 'Esta é uma mensagem de erro.')
    # messages.error(request, 'Esta é outra mensagem de erro.')
    # messages.info(request, 'Esta é uma mensagem informativa.')

    return render(request, 'pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })
    # return render(request, 'pages/home.html', context={
    # 'recipes': [make_recipe() for _ in range(10)],
    # })


def search(request):
    # request.GET.get('q') retorna o mesmo que request.GET['q']
    # porém, quando vazio, o primeiro retorna None
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404('Página não encontrada. 🤪')

    # faz a busca de receitas com base no que foi digitado
    # o Q() permite personalizar o operador lógico: & (and), | (or)
    recipes = Recipe.objects.filter(
        # __icontains faz a funções de um like (contém)
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'pages/search.html', {
        'page_title': f'Search for "{search_term}" | ',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')

    if not recipes:
        raise Http404('Página não encontrada. 🤪')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'Category {recipes.first().category.name} - Category | '
    })


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     pk=id, is_published=True).order_by('-id').first()

    # if not recipe:
    #     raise Http404('Página não encontrada. :(')

    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True
    )

    return render(request, 'pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
