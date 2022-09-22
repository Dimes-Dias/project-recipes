from django.test import TestCase
from recipes import models

# Você pode criar uma classe com um nome qualquer
# Os métodos desta classe são para fornecer dados
# para os testes da classe RecipeViewsTest.


class RecipeTestBase(TestCase):

    # ---------------------------------------------------------------------------------
    # Este método padrão é axecutado automaticamente antes
    # de cada método de teste
    # ---------------------------------------------------------------------------------

    # Inclui objetos a serem testados no banco do teste...
    # Esses objetos estarão disponíveis para todos os métodos de teste criados.
    # Esse banco de teste é criado e excluído ao final do teste
    # pelo próprio pytest automaticamente...
    # Isso pq o pytest não usa o banco da aplicação em si

    def setUp(self) -> None:
        category = models.Category.objects.create(name='Category Test')
        author = models.User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = models.Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        return super().setUp()

    # ---------------------------------------------------------------------------------
    # Este método padrão é axecutado automaticamente depois
    # de cada método de teste.
    # ---------------------------------------------------------------------------------

    def tearDown(self) -> None:
        return super().tearDown()
