from django.db.models import Q
import django_filters
from .models import Ad, ExchangeProposal


class AdFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='keyword_search',
        label='Поиск по названию и описанию'
    )

    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='iexact',
        label='Категория'
    )

    condition = django_filters.CharFilter(
        field_name='condition',
        lookup_expr='iexact',
        label='Состояние'
    )

    class Meta:
        model = Ad
        fields = []

    def keyword_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(description__icontains=value)
            )
        return queryset


class ExchangeProposalFilter(django_filters.FilterSet):
    class Meta:
        model = ExchangeProposal
        fields = {
            'ad_sender': ['exact'],
            'ad_receiver': ['exact'],
            'status': ['exact']
        }
