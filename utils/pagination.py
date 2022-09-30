import math  # inclue funções matemáticas

from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    # calcula a numeração central da paginação
    # math.ceil() -> arredonda pra cima
    middle_range = math.ceil(qty_pages / 2)

    total_pages = len(page_range)

    # obriga a página corrente a ficar dentro dos limites da lista
    current_page = page_range[0] if current_page < page_range[0] else current_page  # noqa E501
    current_page = page_range[-1] if current_page > page_range[-1] else current_page    # noqa E501

    # calcula a numeração inicial de página
    start_range = (current_page - middle_range) if current_page > middle_range else 0  # noqa E501

    # calcula a numeração final de página
    if (page_range[-1] - middle_range) < current_page:
        stop_range = page_range[-1]
        # ajusta página inicial nesta condição
        start_range = (total_pages - qty_pages) if qty_pages < total_pages else 0  # noqa E501
    else:
        stop_range = start_range + qty_pages

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': (current_page > middle_range) and (qty_pages < total_pages),  # noqa E501
        'last_page_out_of_range': (stop_range < len(page_range)) and (qty_pages < total_pages),  # noqa E501
    }


def make_pagination(request, queryset, per_page, qty_pages=5):
    # pega o conteúdo do parâmetro ...?page=
    # se não tiver, ou se houver erro na conversão,
    # pega o 1 como padrão
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    # cria as páginas com Paginator
    paginator = Paginator(queryset, per_page)  # qtde de itens por página
    page_obj = paginator.get_page(current_page)    # informa a página corrente

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page,
    )

    return page_obj, pagination_range
