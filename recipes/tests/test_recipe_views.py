from django.urls import resolve, reverse
from recipes import models, views

from .test_recipe_base import RecipeTestBase


# Todo método de teste, precisa começar com
# a expressão 'test_'
class RecipeViewsTest(RecipeTestBase):

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de rotas de VIEWs
    # ---------------------------------------------------------------------------------

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertIs(view.func, views.recipe)

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de retorno de status 200 (sucesso) ou
    # 404 (página não encontrada) quando há previsão
    # ---------------------------------------------------------------------------------

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_status_code_200_ok(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_status_code_200_ok(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de retorno do template correto
    # ---------------------------------------------------------------------------------

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_recipe_category_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'pages/category.html')

    def test_recipe_detail_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'pages/recipe-view.html')

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de template sem conteúdo
    # ---------------------------------------------------------------------------------

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        # este teste precisa que a template esteja vazia de objetos recipes
        # para isso, iremos esvaziar recipes com o código abaixo...
        # esse esvaziamento irá funcionar apenas no teste em questão.
        models.Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nenhuma receita encontrada..',
            response.content.decode('utf-8')
        )

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de template com conteúdo
    # ---------------------------------------------------------------------------------

    def test_recipe_home_template_loads_recipes(self):
        # faz a captura do conteúdo do template...
        response = self.client.get(reverse('recipes:home'))

        # exemplo do que pode ser feito...
        # response_recipes = response.context['recipes']
        # self.assertEqual(response_recipes.first().title, 'Recipe Title')

        # transforma o conteúdo capturado do template em texto legígel
        content = response.content.decode('utf-8')

        # verifica se os objetos criatos encontram-se no conteúdo do template
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)

        # ou também pode fazer assim...
        # para checar se existe uma receita no template...
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 1)
