from django.urls import path, include
from .views import (CostDetailView,CostDetailUpdateView,CostDetailDeleteView,CostDetailCreateView,
                    PeopleCreateView,PeopleCreateToCostView,PeopleDeleteView, PeopleUpdateView,
                    CostView,CostCreateView,
                    )

app_name = 'main'


urlpatterns = [
    path("detail/<int:pk>",CostDetailView.as_view(), name='cost_detail'),
    path("update-cost-detail/<int:pk>", CostDetailUpdateView.as_view(), name='update_cost_detail'),
    path("detail/<int:pk>/delete",CostDetailDeleteView.as_view(), name='cost_detail_delete'),
    path("<int:pk>/detail-create",CostDetailCreateView.as_view(), name='cost_detail_create'),

    path("<int:pk>/people-create",PeopleCreateView.as_view(), name='people_create'),
    path("<int:pk>/peoplecreate",PeopleCreateToCostView.as_view(), name='people_create_tocost'),
    path("<int:pk>/people-delete",PeopleDeleteView.as_view(), name='people_delete'),
    path("<int:pk>/people-update",PeopleUpdateView.as_view(), name='people_update'),

    path("<int:pk>",CostView.as_view(), name='cost_view'),
    path("create",CostCreateView.as_view(), name='cost_create'),

    # path("new-create-product/",ProductCreateView.as_view(), name='new_create_product'),
    # path("update-product/<int:pk>",ProductUpdateView.as_view(), name='update_product'),
    # path("orders/",OrderListView.as_view(), name='orders'),
    # path("orders/<int:pk>",OrderDetailView.as_view(), name='order_detail'),
    # path("orders/<int:pk>/update",OrderUpdateView.as_view(), name='order_update'),
    # path("orders/<int:pk>/delete",OrderDeleteView.as_view(), name='order_delete'),
    # path("create-order/",create_order, name='create_order'),
    # path("new-create-order/",OrderCreateView.as_view(), name='new-create_order'),
]