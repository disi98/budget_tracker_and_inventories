from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm
from inventory.models import InventoryItem

@login_required
def home_dashboard(request):
    return render(request, "dashboard/home_dashboard.html")


@login_required
def stock(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.total_price = inventory_item.quantity * inventory_item.price_per_unit
            inventory_item.save()
            return redirect('dashboard:sales_list')
    else:
        form = InventoryItemForm()
    return render(request, 'dashboard/stock.html', {'form': form})