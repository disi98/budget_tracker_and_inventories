from django import forms
from inventory.models import InventoryItem, Category
from django.core.exceptions import ValidationError

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
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    
    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'description', 'quantity', 'price_per_unit', 'transaction_type', 'date']

    def __init__(self, *args, **kwargs):
        super(InventoryItemForm, self).__init__(*args, **kwargs)
        self.fields['transaction_type'].choices = InventoryItem.TRANSACTION_TYPE_CHOICES




class SellItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }),
        required=True
    )
    
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.none(),
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }),
        required=True
    )

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'id': 'description',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'rows': 4,
    }))
    
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Quantity',
            'id': 'quantity',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'required': True,
        })
    )
    
    price_per_unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Price per Unit',
        'id': 'price_per_unit',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'required': True,
    }))

    class Meta:
        model = InventoryItem
        fields = ['category', 'item', 'description', 'quantity']

    def __init__(self, *args, **kwargs):
        super(SellItemForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['item'].queryset = InventoryItem.objects.filter(category_id=category_id, transaction_type=InventoryItem.STOCKING)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item'].queryset = self.instance.category.inventory_items.filter(transaction_type=InventoryItem.STOCKING)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')

        if item and quantity:
            available_stock = item.available_stock()
            if quantity > available_stock:
                raise ValidationError(f"Cannot sell {quantity} items. Only {available_stock} items in stock.")
        
        return cleaned_data
    

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'enter category',
            'id': 'enter-category',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'required': True,
        })
    )
    class Meta:
        model = Category
        fields = ['name']