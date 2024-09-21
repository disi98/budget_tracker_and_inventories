from django import forms
from inventory.models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'description', 'quantity', 'price_per_unit', 'transaction_type']