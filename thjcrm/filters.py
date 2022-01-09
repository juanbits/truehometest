from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter, FilterSet, DateFilter, CharFilter
from .models import Activity

class ActivityFilter(FilterSet):
    schedule = DateFromToRangeFilter(field_name="schedule")
    status = CharFilter(field_name="status",lookup_expr='icontains',label='Status')

    class Meta:
        model = Activity
        fields = ['schedule']