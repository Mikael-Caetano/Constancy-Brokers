from rest_framework.pagination import PageNumberPagination


class SelectPaginator(PageNumberPagination):
    page_size = 20


class ListTradesPaginator(PageNumberPagination):
    page_size = 30