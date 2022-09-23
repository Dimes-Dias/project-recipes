from django.test import TestCase
from recipes import models

# Você pode criar uma classe com um nome qualquer
# Os métodos desta classe são para fornecer dados
# para os testes da classe RecipeViewsTest.


class RecipeTestBase(TestCase):

    # ---------------------------------------------------------------------------------
    # setUp()
    # Este método padrão é axecutado automaticamente antes
    # de cada método de teste
    # ---------------------------------------------------------------------------------

    # Inclui objetos a serem testados no banco do teste...
    # Esses objetos estarão disponíveis para todos os métodos de teste criados.
    # Esse banco de teste é criado e excluído ao final do teste
    # pelo próprio pytest automaticamente...
    # Isso pq o pytest não usa o banco da aplicação em si

    def setUp(self) -> None:
        # o exemplo abaixo serve apenas para indicar o que poderia ser feito...
        # assim, não é necessário especificar este método na classe
        '''
        category = self.make_category()
        author = self.make_author()
        self.make_recipe(input_category=category, input_author=author)
        '''
        return super().setUp()

    # ---------------------------------------------------------------------------------
    # tearDown()
    # Este método padrão é axecutado automaticamente depois
    # de cada método de teste.
    # Como ele não possui nenhuma instrução adicional, não há a necessidade
    # de tê-lo no corpo desta classe.
    # ---------------------------------------------------------------------------------

    def tearDown(self) -> None:
        return super().tearDown()

    def make_category(self, name='Category Test'):
        return models.Category.objects.create(name=name)

    def make_author(
        self,
        user='user',
        name='name',
        username='username',
        password='123456',
        email='username@email.com'
    ):
        return models.User.objects.create_user(
            first_name=user,
            last_name=name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return models.Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published
        )
