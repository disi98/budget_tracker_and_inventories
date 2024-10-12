from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    STOCKING = 'ST'
    SOLD = 'SO'
    TRANSACTION_TYPE_CHOICES = [
        (STOCKING, 'Stocking'),
        (SOLD, 'Sold'),
    ]

    category = models.ForeignKey(Category, related_name='inventory_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    quantity = models.FloatField(null=False)
    total_price = models.FloatField(blank=True)
    price_per_unit = models.FloatField(blank=True)
    date = models.DateField(default=models.DateField(auto_now_add=True))
    transaction_type = models.CharField(
        max_length=2,
        choices=TRANSACTION_TYPE_CHOICES,
        default=STOCKING,
    )

    class Meta:
        ordering = ('date', 'transaction_type')

    def __str__(self):
        return f"{self.name} ({self.get_transaction_type_display()})"

    @staticmethod
    def total_quantity_in_stock():
        stocked = InventoryItem.objects.filter(transaction_type=InventoryItem.STOCKING).aggregate(total=models.Sum('quantity'))['total'] or 0
        sold = InventoryItem.objects.filter(transaction_type=InventoryItem.SOLD).aggregate(total=models.Sum('quantity'))['total'] or 0
        return stocked - sold

    @staticmethod
    def total_quantity_sold():
        return InventoryItem.objects.filter(transaction_type=InventoryItem.SOLD).aggregate(total=models.Sum('quantity'))['total'] or 0

    @staticmethod
    def total_sales():
        return InventoryItem.objects.filter(transaction_type=InventoryItem.SOLD).aggregate(total=models.Sum('total_price'))['total'] or 0

    @staticmethod
    def total_profit():
        return InventoryItem.total_sales() - InventoryItem.objects.filter(transaction_type=InventoryItem.STOCKING).aggregate(total=models.Sum('total_price'))['total'] or 0
 
    def available_stock(self):
        total_stocked = InventoryItem.objects.filter(
            category=self.category,
            name=self.name,
            transaction_type=self.STOCKING
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        total_sold = InventoryItem.objects.filter(
            category=self.category,
            name=self.name,
            transaction_type=self.SOLD
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        return total_stocked - total_sold

    def update_quantity(self, quantity_change):
        if self.transaction_type == self.STOCKING:
            self.quantity += quantity_change
        elif self.transaction_type == self.SOLD:
            available_stock = self.available_stock()
            if quantity_change > available_stock:
                raise ValidationError(f"Cannot sell {quantity_change} items. Only {available_stock} items in stock.")
            self.quantity -= quantity_change
        self.save()