from django.test import TestCase


# Você pode criar uma classe com um nome qualquer
class RecipeURLsTest(TestCase):
    # Todo método de teste, precisa começar com
    # a expressão 'test_'
    def test_the_pytest_is_ok(self):
        print('Olá Dimes Dias')
        assert 1 == 1, 'Um não é igual a dois'
