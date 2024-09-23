from django import forms
from inventory.models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'description', 'quantity', 'price_per_unit', 'transaction_type']

        def __init__(self, *args, **kwargs):
            super(InventoryItemForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({
                    'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md focus:border-blue-500 focus:outline-none focus:ring'
                })