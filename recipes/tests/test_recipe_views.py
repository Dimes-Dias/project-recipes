from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


# Todo método de teste, precisa começar com
# a expressão 'test_'
# self.fail('mensagem') -> provocar um erro no método específico, como um lembrete      # noqa E501
# @skip('mensagem') -> uma linha acima da classe ou do método, para pular aquele teste  # noqa E501
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

    def test_recipe_search_user_correct_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de retorno de status 200 (sucesso) ou
    # 404 (página não encontrada) quando há previsão
    # ---------------------------------------------------------------------------------

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_status_code_200_ok(self):
        # make_recipe()
        # método criado em RecipeTestBase para criar dados de teste
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_status_code_200_ok(self):
        # make_recipe()
        # método criado em RecipeTestBase para criar dados de teste
        self.make_recipe()
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

    def test_recipe_search_raises_404_if_search_term(self):
        response = self.client.get(
            reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de retorno do template correto
    # ---------------------------------------------------------------------------------

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'pages/search.html')

    def test_recipe_category_view_loads_correct_template(self):
        # make_recipe()
        # método criado em RecipeTestBase para criar dados de teste
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'pages/category.html')

    def test_recipe_detail_view_loads_correct_template(self):
        # make_recipe()
        # método criado em RecipeTestBase para criar dados de teste
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'pages/recipe-view.html')

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de template sem conteúdo
    # ---------------------------------------------------------------------------------

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nenhuma receita encontrada..',
            response.content.decode('utf-8')
        )

    # ---------------------------------------------------------------------------------
    # Estes métodos contém testes de template com conteúdo (se o conteúdo está correto) # noqa E501
    # ---------------------------------------------------------------------------------

    def test_recipe_home_template_loads_recipes(self):
        # make_recipe()
        # método criado em RecipeTestBase para criar dados de teste
        self.make_recipe(preparation_time=2, preparation_time_unit='Horas')

        # faz a captura do conteúdo do template...
        response = self.client.get(reverse('recipes:home'))

        # exemplo do que pode ser feito...
        # response_recipes = response.context['recipes']
        # self.assertEqual(response_recipes.first().title, 'Recipe Title')

        # transforma o conteúdo capturado do template em texto legígel
        content = response.content.decode('utf-8')

        # verifica se os objetos criatos encontram-se no conteúdo do template
        self.assertIn('Recipe Title', content)
        self.assertIn('2 Horas', content)
        self.assertIn('5 Porções', content)

        # ou também pode fazer assim...
        # para checar se existe uma receita no template...
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'Isto é uma categoria de test'

        recipe = self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id}))  # noqa E501

        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'Isto é uma página de detalhe - abre uma receita'

        recipe = self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)
