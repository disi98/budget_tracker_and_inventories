import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64
from datetime import datetime
from django.db.models import Sum
from inventory.models import InventoryItem

def get_inventory_data(request):
    date_str = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Get data for the selected date
    daily_stock = InventoryItem.objects.filter(date=selected_date, transaction_type=InventoryItem.STOCKING).aggregate(total=Sum('quantity'))['total'] or 0
    daily_sales = InventoryItem.objects.filter(date=selected_date, transaction_type=InventoryItem.SOLD).aggregate(total=Sum('quantity'))['total'] or 0

    daily_stock_price = InventoryItem.objects.filter(date=selected_date, transaction_type=InventoryItem.STOCKING).aggregate(total=Sum('total_price'))['total'] or 0
    daily_sales_price = InventoryItem.objects.filter(date=selected_date, transaction_type=InventoryItem.SOLD).aggregate(total=Sum('total_price'))['total'] or 0

    # Get sales data for each item
    items_sold = InventoryItem.objects.filter(
        transaction_type=InventoryItem.SOLD,
        date=selected_date
    ).values('name').annotate(total_sold=Sum('quantity')).order_by('name')

    item_names_sold = [item['name'] for item in items_sold]
    quantities_sold = [item['total_sold'] for item in items_sold]

    # Get stock data for each item
    items_in_stock = InventoryItem.objects.filter(
        transaction_type=InventoryItem.STOCKING,
        date=selected_date
    ).values('name').annotate(total_stocked=Sum('quantity')).order_by('name')

    item_names_stocked = [item['name'] for item in items_in_stock]
    quantities_stocked = [item['total_stocked'] for item in items_in_stock]

    # Create Matplotlib plot for items sold with figsize 8x6
    fig_sold, ax_sold = plt.subplots(figsize=(10, 6))
    ax_sold.plot(item_names_sold, quantities_sold, marker="o", color='r', label='Items Sold')
    # ax_sold.set_title(f"Items Sold on {selected_date}")
    ax_sold.set_xlabel('Items')
    ax_sold.set_ylabel('Quantity Sold')
    ax_sold.grid(True)
    plt.xticks(rotation=45)
    plt.legend()

    # Save the sold plot to a BytesIO object
    buf_sold = BytesIO()
    plt.savefig(buf_sold, format='png')
    buf_sold.seek(0)
    plt.close(fig_sold)

    # Encode the sold image to base64 to be rendered in the template
    image_sold_base64 = base64.b64encode(buf_sold.getvalue()).decode('utf-8')

    # Create Matplotlib plot for items stocked with figsize 8x6
    fig_stocked, ax_stocked = plt.subplots(figsize=(10, 6))
    ax_stocked.plot(item_names_stocked, quantities_stocked, marker="o", color='b', label='Items Stocked')
    # ax_stocked.set_title(f"Items Stocked on {selected_date}")
    ax_stocked.set_xlabel('Items')
    ax_stocked.set_ylabel('Quantity Stocked')
    ax_stocked.grid(True)
    plt.xticks(rotation=30)
    plt.legend()

    # Save the stocked plot to a BytesIO object
    buf_stocked = BytesIO()
    plt.savefig(buf_stocked, format='png')
    buf_stocked.seek(0)
    plt.close(fig_stocked)

    # Encode the stocked image to base64 to be rendered in the template
    image_stocked_base64 = base64.b64encode(buf_stocked.getvalue()).decode('utf-8')

    context = {
        'selected_date': selected_date,
        'daily_stock': daily_stock,
        'daily_sales': daily_sales,
        'daily_stock_price': daily_stock_price,
        'daily_sales_price': daily_sales_price,
        'image_sold_base64': image_sold_base64,
        'image_stocked_base64': image_stocked_base64,
    }
    return render(request, 'reports/get_inventory_data.html', context)