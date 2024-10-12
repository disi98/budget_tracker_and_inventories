from django.urls import path

from .views import get_inventory_data

app_name = "reports"

urlpatterns = [
    path('api/inventory-data/', get_inventory_data, name='get_inventory_data'),
]