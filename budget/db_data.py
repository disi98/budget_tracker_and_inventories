import os
import django
import csv
import random
from datetime import timedelta
from faker import Faker
from django.utils import timezone

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget.settings')

# Setup Django
django.setup()

# Now import your models
from inventory.models import Category, InventoryItem

fake = Faker()

def generate_inventory_data(csv_filename, num_records):

    # Get existing categories to associate with inventory items
    categories = list(Category.objects.values_list('id', flat=True))
    
    if not categories:
        print("No categories available. Please create categories first.")
        return

    start_date = timezone.now() - timedelta(days=60)  # Start two months ago
    end_date = timezone.now()

    with open(csv_filename, mode='w', newline='') as csv_file:
        fieldnames = ['category_id', 'name', 'description', 'quantity', 'total_price', 'price_per_unit', 'date', 'transaction_type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for _ in range(num_records):
            transaction_type = random.choice([InventoryItem.STOCKING, InventoryItem.SOLD])
            if transaction_type == InventoryItem.STOCKING:
                quantity = random.randint(10, 30)  # Stocking between 10 and 30
            else:
                quantity = random.randint(10, 30)  # Selling between 10 and 30

            price_per_unit = random.uniform(5.0, 100.0)  # Random price between 5 and 100
            total_price = price_per_unit * quantity

            # Generate a random date within the last two months
            random_date = start_date + timedelta(days=random.randint(0, 60))

            # Create a random item name
            item_name = fake.word().capitalize()

            writer.writerow({
                'category_id': random.choice(categories),
                'name': item_name,
                'description': fake.sentence(),
                'quantity': quantity,
                'total_price': round(total_price, 2),
                'price_per_unit': round(price_per_unit, 2),
                'date': random_date.strftime('%Y-%m-%d'),
                'transaction_type': transaction_type,
            })

    print(f"Generated {num_records} records and saved to {csv_filename}")

# Usage
generate_inventory_data('inventory_data.csv', 100)
