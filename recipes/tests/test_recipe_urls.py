from django.test import TestCase
from django.urls import reverse
from recipes import views


# Você pode criar uma classe com um nome qualquer
# Esta classe contém métodos de test de rotas de URLs
class RecipeURLsTest(TestCase):
    # Todo método de teste, precisa começar com
    # a expressão 'test_'

    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')
