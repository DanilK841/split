from django.urls import path, include, register_converter
from .converters import HyphenlessUUIDConverter
from .views import (CostDetailUpdateView,CostDetailDeleteView,CostDetailCreateView,
                    PeopleCreateView,PeopleDeleteView, PeopleUpdateView,
                    CostView,CostCreateView,
                    )

app_name = 'main'

register_converter(HyphenlessUUIDConverter, 'hyphenless_uuid')
urlpatterns = [

    path("update-cost-detail/<uuid:pk>", CostDetailUpdateView.as_view(), name='update_cost_detail'),
    path("detail/<uuid:pk>/delete",CostDetailDeleteView.as_view(), name='cost_detail_delete'),
    path("<uuid:pk>/detail-create",CostDetailCreateView.as_view(), name='cost_detail_create'),

    path("<uuid:pk>/people-create",PeopleCreateView.as_view(), name='people_create'),
    path("<uuid:pk>/people-delete",PeopleDeleteView.as_view(), name='people_delete'),
    path("<uuid:pk>/people-update",PeopleUpdateView.as_view(), name='people_update'),

    path("<uuid:pk>>",CostView.as_view(), name='cost_view'),
    path("create",CostCreateView.as_view(), name='cost_create'),

]