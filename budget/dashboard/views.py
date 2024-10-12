from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm, SellItemForm, CategoryForm
from inventory.models import InventoryItem, Category
from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import models


@require_POST
def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    return JsonResponse({'success': True})

@login_required
def home_dashboard(request):
    total_profit = InventoryItem.objects.filter(transaction_type=InventoryItem.STOCKING).aggregate(stock_cost=models.Sum("total_price"))['stock_cost'] or 0
    total_sales = InventoryItem.total_sales()   
    sold = InventoryItem.total_quantity_sold()
    instock = InventoryItem.total_quantity_in_stock()
    alltime_stock = sold + instock
    return render(request, "dashboard/home_dashboard.html", {"instock": instock, "sold": sold, "alltime_stock": alltime_stock, "total_sales": total_sales, "total_profit": total_profit})


@login_required
def stock(request):
    item = InventoryItem.objects.filter(transaction_type=InventoryItem.STOCKING).order_by('-date')
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
    items = InventoryItem.objects.filter(transaction_type=InventoryItem.SOLD)
    paginator = Paginator(items, 10)  # Show 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    instock = InventoryItem.total_quantity_in_stock()
    sold = InventoryItem.total_quantity_sold()

    return render(request, 'dashboard/sold.html', {
        'page_obj': page_obj,
        'instock': instock,
        'sold': sold
    })


@login_required
def stock_list(request):
    stock_items = InventoryItem.objects.filter(transaction_type=InventoryItem.STOCKING).order_by('-date')
    paginator = Paginator(stock_items, 10)  # Show 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    items_with_stock = [
        {
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'available_stock': round(item.available_stock())
        }
        for item in page_obj
    ]
    instock = InventoryItem.total_quantity_in_stock()
    sold = InventoryItem.total_quantity_sold()
    return render(request, 'dashboard/stock_list.html', {
        'page_obj': page_obj,
        'items': items_with_stock,
        'instock': instock,
        'sold': sold
    })

@login_required
def sell_item(request):

    instock = InventoryItem.total_quantity_in_stock()
    sold = InventoryItem.total_quantity_sold()


    total_in_stock = InventoryItem.total_quantity_in_stock()
    total_sold = InventoryItem.total_quantity_sold()

    if request.method == 'POST':
        form = SellItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            InventoryItem.objects.create(
                category=item.category,
                name=item.name,
                description=item.description,
                quantity=quantity,
                total_price=item.price_per_unit * quantity,
                price_per_unit=item.price_per_unit,
                transaction_type=InventoryItem.SOLD
            )
            return redirect('dashboard:sold')
    else:
        form = SellItemForm()

    context = {
        'form': form,
        'total_in_stock': total_in_stock,
        'total_sold': total_sold,
        'instock': instock,
        'sold': sold,
    }
    return render(request, 'dashboard/sell_item.html', context)

def get_items(request):
    category_id = request.GET.get('category_id')
    items = InventoryItem.objects.filter(category_id=category_id, transaction_type=InventoryItem.STOCKING).values('id', 'name')
    return JsonResponse(list(items), safe=False)



def add_category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'save_and_add_another' in request.POST:
                return redirect('dashboard:add_category')
            else:
                return redirect('dashboard:sold')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form, 'category': categories})

