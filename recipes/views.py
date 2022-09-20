from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.recipes.factory import make_recipe

from recipes.models import Recipe


def home(request):
    # recipes = Recipe.objects.all().order_by('-id')
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'pages/home.html', context={
        'recipes': recipes,
    })
    # return render(request, 'pages/home.html', context={
    # 'recipes': [make_recipe() for _ in range(10)],
    # })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')

    if not recipes:
        raise Http404('Página não encontrada. 🤪')

    return render(request, 'pages/category.html', context={
        'recipes': recipes,
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
