from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views


# Você pode criar uma classe com um nome qualquer
# Esta classe contém métodos de test de rotas de VIEWs
class RecipeViewsTest(TestCase):
    # Todo método de teste, precisa começar com
    # a expressão 'test_'

    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
