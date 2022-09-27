from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes import models

from .test_recipe_base import RecipeTestBase


# Esta classe deve testar apenas partes lógicas de models,
# e não mecanismos do django, pois seria disperdício de recurso e tempo.
class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    # ---------------------------------------------------------------------------------
    # Métodos de validação de limitação de quantidade de caracteres permitidos
    # ---------------------------------------------------------------------------------

    # testa se levanta erro quando entrar mais de 65 letras em title
    # nesse caso, o teste deve passar caso isso ocorra
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        # altera o title para exceder 65 caracteres
        self.recipe.title = 'A' * 66

        # Se usar self.recipe.save(), o django salvaria o texto
        # mesmo o texto (title) excedendo 65 caracteres.
        # Nesse código, ao se fazer validação, é esperado que o
        # teste levante um ValidationError.
        # Como o erro já é esperado, o teste passa sem problemas.
        # Porém, se (self.recipe.title = 'A' * 65), ou seja,
        # se o texto não excedesse 65 caracteres, o teste iria falhar,
        # pois o ValidationError seria esperado, mas não aconteceria.
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    # podemos executar o procedimento acima para vários campos,
    # como no exemplo a seguir.
    # É necessário instalar o pacote (pip install parameterized),
    # e importar (from parameterized import parameterized)
    @parameterized.expand([
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    # O método será executado para cada entrada de parâmetro
    def test_recipe_fields_max_length(self, field, max_length):
        # setattr() atribui a um campo um valor de forma dinâmica
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = models.Recipe(
            category=self.make_category(name='Teste Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-for-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
