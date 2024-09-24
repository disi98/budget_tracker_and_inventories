from django import forms
from inventory.models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    category = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Item Name',  # Placeholder for the name
        'id': 'name',  # ID for the name input
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,  # Make it a required field
    }))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description',  # Placeholder for the description
        'id': 'description',  # ID for the description input
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'rows': 4,  # Number of rows for the textarea
    }))
    
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Quantity',  # Placeholder for quantity
        'id': 'quantity',  # ID for the quantity input
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,  # Make it a required field
    }))
    
    price_per_unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Price per Unit',  # Placeholder for price
        'id': 'price_per_unit',  # ID for the price input
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,  # Make it a required field
    }))
    
    transaction_type = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    
    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'description', 'quantity', 'price_per_unit', 'transaction_type']
