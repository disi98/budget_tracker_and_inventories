from django import forms
from inventory.models import InventoryItem, Category

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        })
    )
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Item Name',
        'id': 'name',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,
    }))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'id': 'description',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'rows': 4,
    }))
    
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Quantity',
        'id': 'quantity',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,
    }))
    
    price_per_unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Price per Unit',
        'id': 'price_per_unit',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,
    }))
    
    transaction_type = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    
    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'description', 'quantity', 'price_per_unit', 'transaction_type']

    def __init__(self, *args, **kwargs):
        super(InventoryItemForm, self).__init__(*args, **kwargs)
        self.fields['transaction_type'].choices = InventoryItem.TRANSACTION_TYPE_CHOICES