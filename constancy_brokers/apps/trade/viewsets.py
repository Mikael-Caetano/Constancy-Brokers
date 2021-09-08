import datetime
from django.db.models import (
    Q,
    Count,
    Value,
    Sum,
    FloatField,
    DateTimeField,
)
from django.db.models.functions import (
    Concat,
    Coalesce,
    Cast,
    TruncMinute,
)

from rest_framework import serializers, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .paginators import SelectPaginator, ListTradesPaginator
from .models import Provider, Currency, Pair, Trade
from .serializers import (
    BlotterTradesSerializer,
    BlotterTradesGraphSerializer,
    TradeSerializer,
    ProviderSerializer,
    CurrencySerializer,
    PairSerializer,
)
from .permissions import IsProviderAdmin


class ProviderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsProviderAdmin)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProviderSerializer

    def get_queryset(self):
        return Provider.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Provider sucessfully created!"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Provider sucessfully updated!"}, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"detail": "Provider sucessfully destroyed"},
            status=status.HTTP_200_OK,
        )


class CurrencyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsProviderAdmin)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Currency sucessfully created!"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Currency sucessfully updated!"}, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"detail": "Currency sucessfully destroyed"},
            status=status.HTTP_200_OK,
        )


class PairViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsProviderAdmin)
    authentication_classes = (TokenAuthentication,)
    serializer_class = PairSerializer

    def get_queryset(self):
        return Pair.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Pair sucessfully created!"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Pair sucessfully updated!"}, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"detail": "Pair sucessfully destroyed"},
            status=status.HTTP_200_OK,
        )


class TradeViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TradeSerializer

    def get_queryset(self):
        return Trade.objects.filter(trader=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Trade sucessfully created!"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Trade sucessfully updated!"}, status=status.HTTP_200_OK
        )


class SelectProviderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    class OutputSerializer(serializers.ModelSerializer):
        value = serializers.SerializerMethodField("get_id")
        label = serializers.SerializerMethodField("get_acronym")

        class Meta:
            model = Provider
            fields = ("value", "label")

        def get_id(self, obj):
            return obj.id

        def get_acronym(self, obj):
            return obj.acronym

    def get(self, request):
        _filter = Q()

        search = request.GET.get("search", None)
        if search is not None:
            _filter.add(
                Q(Q(name__icontains=search) | Q(acronym__icontains=search)), Q.AND
            )

        providers = Provider.objects.filter(_filter).distinct().order_by("acronym")
        serialized_providers = self.OutputSerializer(providers, many=True).data

        select_data = {}
        paginator = SelectPaginator()
        result_page = paginator.paginate_queryset(serialized_providers, request)
        select_data["next"] = paginator.get_next_link()
        select_data["previous"] = paginator.get_previous_link()
        select_data["results"] = result_page

        return Response(select_data, status=status.HTTP_200_OK)


class SelectCurrencyPairView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    class OutputSerializer(serializers.ModelSerializer):
        value = serializers.SerializerMethodField("get_id")
        label = serializers.SerializerMethodField("get_joined_acronyms")

        class Meta:
            model = Pair
            fields = ("value", "label")

        def get_id(self, obj):
            return obj.id

        def get_joined_acronyms(self, obj):
            return obj.joined_acronyms

    def get(self, request):
        _filter = Q()

        search = request.GET.get("search", None)
        if search is not None:
            _filter.add(
                Q(
                    Q(from_currency__name__icontains=search)
                    | Q(to_currency__name__icontains=search)
                    | Q(annotated_joined_acronyms__icontains=search)
                ),
                Q.AND,
            )

        pairs = (
            Pair.objects.annotate(
                annotated_joined_acronyms=Concat(
                    "from_currency__acronym", Value("/"), "to_currency__acronym"
                )
            )
            .filter(_filter)
            .distinct()
            .order_by("annotated_joined_acronyms")
        )
        serialized_pairs = self.OutputSerializer(pairs, many=True).data

        select_data = {}
        paginator = SelectPaginator()
        result_page = paginator.paginate_queryset(serialized_pairs, request)
        select_data["next"] = paginator.get_next_link()
        select_data["previous"] = paginator.get_previous_link()
        select_data["results"] = result_page

        return Response(select_data, status=status.HTTP_200_OK)


class BlotterTradesViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    default_serializer_class = BlotterTradesSerializer
    serializer_classes = {"graph": BlotterTradesGraphSerializer}

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Trade.objects.filter(trader=self.request.user)

    def list(self, request):
        user = request.user

        pairs = request.GET.getlist("pairs", [])
        min_price = request.GET.get("min_price", None)
        max_price = request.GET.get("max_price", None)
        min_quantity = request.GET.get("min_quantity", None)
        max_quantity = request.GET.get("max_quantity", None)

        _filter = Q(trader=user)

        try:
            start_time = datetime.datetime.strptime(
                request.GET.get("start", None), "%d/%m/%Y %H:%M"
            )
        except:
            start_time = None

        try:
            end_time = datetime.datetime.strptime(
                request.GET.get("end", None), "%d/%m/%Y %H:%M"
            )
        except:
            end_time = None

        if pairs:
            _filter.add(
                Q(pair__in=pairs),
                Q.AND,
            )

        if min_price is not None:
            _filter.add(Q(price__gte=min_price), Q.AND)

        if max_price is not None:
            _filter.add(Q(price__lte=max_price), Q.AND)

        if min_quantity is not None:
            _filter.add(Q(quantity__gte=min_quantity), Q.AND)

        if max_quantity is not None:
            _filter.add(Q(quantity__lte=max_quantity), Q.AND)

        if start_time is not None:
            _filter.add(Q(date__gte=start_time), Q.AND)

        if end_time is not None:
            _filter.add(Q(date__lte=end_time), Q.AND)

        trades = (
            Trade.objects.filter(_filter)
            .only("id", "date", "pair", "price", "quantity")
            .select_related("pair")
            .distinct()
            .order_by("-date")
        )
        serialized_trades = self.get_serializer(trades, many=True).data

        select_data = {}
        paginator = ListTradesPaginator()
        result_page = paginator.paginate_queryset(serialized_trades, request)
        select_data["next"] = paginator.get_next_link()
        select_data["previous"] = paginator.get_previous_link()
        select_data["results"] = result_page

        return Response(select_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def graph(self, request):
        user = request.user

        providers = request.GET.getlist("providers", [])

        _filter = Q(trader=user)

        try:
            start_time = datetime.datetime.strptime(
                request.GET.get("start", None), "%d/%m/%Y %H:%M"
            )
        except:
            start_time = None

        try:
            end_time = datetime.datetime.strptime(
                request.GET.get("end", None), "%d/%m/%Y %H:%M"
            )
        except:
            end_time = None

        if providers:
            _filter.add(
                Q(provider__in=providers),
                Q.AND,
            )

        if start_time is not None:
            _filter.add(Q(date__gte=start_time), Q.AND)

        if end_time is not None:
            _filter.add(Q(date__lte=end_time), Q.AND)

        trades = (
            Trade.objects.filter(_filter)
            .distinct()
            .values("id", "date", "price")
            .order_by("date")
        )

        serialized_trades = self.get_serializer(trades, many=True).data

        return Response(serialized_trades, status=status.HTTP_200_OK)


class MarketGraphView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        providers = request.GET.getlist("providers", [])
        pair = request.GET.get("pair", None)

        try:
            start_time = datetime.datetime.strptime(
                request.GET.get("start", None), "%d/%m/%Y %H:%M"
            )
        except:
            start_time = None

        try:
            end_time = datetime.datetime.strptime(
                request.GET.get("end", None), "%d/%m/%Y %H:%M"
            )
        except:
            end_time = None

        _filter = Q()

        if start_time is not None:
            _filter.add(Q(date__gte=start_time), Q.AND)

        if end_time is not None:
            _filter.add(Q(date__lte=end_time), Q.AND)

        if pair is not None:
            _filter.add(Q(pair=pair), Q.AND)

        trades = (
            Trade.objects.filter(
                _filter,
            )
            .annotate(
                trunc_minute=Cast(TruncMinute("date"), DateTimeField()),
            )
            .values("trunc_minute")
            .annotate(
                overall=Coalesce(
                    Cast(Sum("price"), FloatField())
                    / Cast(Count("provider", distinct=True), FloatField()),
                    0,
                )
            )
            .values("trunc_minute", "overall")
            .order_by("trunc_minute")
        )

        data_list = []
        providers = Provider.objects.filter(id__in=providers)
        for provider in providers:
            provider_data = trades.annotate(
                vwap=Coalesce(
                    (
                        (
                            Cast(
                                Sum("price", filter=Q(_filter, provider=provider)),
                                FloatField(),
                            )
                            * Cast(
                                Sum("quantity", filter=Q(_filter, provider=provider)),
                                FloatField(),
                            )
                        )
                        / Cast(
                            Sum("quantity", filter=Q(_filter, provider=provider)),
                            FloatField(),
                        )
                    ),
                    0,
                ),
                feed=Coalesce(
                    Cast(
                        Sum("price", filter=Q(_filter, trader=user, provider=provider)),
                        FloatField(),
                    ),
                    0,
                ),
            ).values("vwap", "feed", "trunc_minute")

            for data in provider_data:
                data[provider.acronym.lower() + "_vwap"] = data.pop("vwap")
                data[provider.acronym.lower() + "_feed"] = data.pop("feed")
                data_list.append(data)

        results = []
        for trade in trades:
            providers_data = list(
                filter(
                    lambda data: data["trunc_minute"] == trade["trunc_minute"],
                    data_list,
                )
            )

            for provider_data in providers_data:
                for field in provider_data:
                    if field != "trunc_minute":
                        trade[field] = provider_data[field]
                    else:
                        trade["date"] = {
                            "date": provider_data[field].strftime("%Y/%m/%d"),
                            "time": provider_data[field].strftime("%H:%M:%S.%f")[:-3],
                        }

            results.append(trade)

        for result in results:
            del result["trunc_minute"]

        return Response(results, status=status.HTTP_200_OK)
