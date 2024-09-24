from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm
from inventory.models import InventoryItem

@login_required
def home_dashboard(request):
    sold = InventoryItem.total_quantity_sold()
    instock = InventoryItem.total_quantity_in_stock()
    return render(request, "dashboard/home_dashboard.html", {"instock": instock, "sold": sold})


@login_required
def stock(request):
    instock = InventoryItem.total_quantity_in_stock()
    sold = InventoryItem.total_quantity_sold
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.total_price = inventory_item.quantity * inventory_item.price_per_unit
            inventory_item.save()
            return redirect('dashboard:stock')
    else:
        form = InventoryItemForm()
    return render(request, 'dashboard/stock.html', {'form': form, 'instock': instock, 'sold': sold})

@login_required
def sold(request):
    items = InventoryItem.objects.all()

    instock = InventoryItem.total_quantity_in_stock()
    sold = InventoryItem.total_quantity_sold()

    sold_items = InventoryItem.objects.filter(transaction_type=InventoryItem.SOLD)

    return render(request, 'dashboard/sold.html', {'items': items, 'instock': instock, 'sold': sold, 'sold_items': sold_items})