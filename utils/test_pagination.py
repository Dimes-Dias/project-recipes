from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    # testa a primeira página, se retorna a lista de páginas corretamente
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    # testa a página do meio, se retorna a lista de páginas corretamente
    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )
        self.assertEqual([9, 10, 11, 12], pagination['pagination'])

    # testa a última página, se retorna a lista de páginas corretamente
    def test_last_range_is_static_if_current_page_is_last(self):  # noqa E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
