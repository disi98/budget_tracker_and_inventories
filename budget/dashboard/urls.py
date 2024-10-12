from django.urls import path


from .views import home_dashboard, stock, sold, stock_list, sell_item, get_items, delete_inventory_item, add_category

app_name = "dashboard"

urlpatterns = [
    path("", home_dashboard, name="home_dashboard"),
    path("stock/", stock, name="stock"),
    path("sold/", sold, name="sold"),
    path("stock_list/", stock_list, name="stock_list"),
    path("sell_item/", sell_item, name="sell_item"),
    path("get_items/", get_items, name="get_items"),
    path('delete-item/<int:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('add-category/', add_category, name='add_category'),
]