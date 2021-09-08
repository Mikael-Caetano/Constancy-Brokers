from django.urls import path, include
from rest_framework.routers import DefaultRouter

from palladris_brokers.apps.trade.viewsets import (
    SelectProviderView,
    SelectCurrencyPairView,
    BlotterTradesViewset,
    MarketGraphView,
    TradeViewSet,
    ProviderViewSet,
    CurrencyViewSet,
    PairViewSet,
)

router = DefaultRouter()
router.register("trades", TradeViewSet, basename="trades")
router.register("providers", ProviderViewSet, basename="providers")
router.register("currencies", CurrencyViewSet, basename="currencies")
router.register("pairs", PairViewSet, basename="pairs")

blotter_router = DefaultRouter()
blotter_router.register("trades", BlotterTradesViewset, basename="blotter-trades")

urlpatterns = [
    path(
        "select-providers/",
        SelectProviderView.as_view(),
        name="select-providers",
    ),
    path(
        "select-currency-pairs/",
        SelectCurrencyPairView.as_view(),
        name="select-currency-pairs",
    ),
    path("blotter/", include(blotter_router.urls)),
    path(
        "market/",
        MarketGraphView.as_view(),
        name="market-graph",
    ),
]

urlpatterns += router.urls