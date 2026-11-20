"""
Django script to populate database with sample data for testing dashboard
Run this with: python manage.py shell < populate_sample_data.py
"""

import os
import django
import datetime
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearningDjango.settings')
django.setup()

from digitaldairy.models import Cow, MilkProductions, Clients, MilkSales, ContactMessage, SemenRecords
from django.contrib.auth.models import User
from accounts.models import UserProfile

print("=" * 60)
print("Starting to populate database with sample data...")
print("=" * 60)

# Clear existing data (optional - comment out if you want to keep existing data)
print("\n1. Clearing existing sample data...")
MilkSales.objects.all().delete()
MilkProductions.objects.all().delete()
ContactMessage.objects.all().delete()
Cow.objects.all().delete()
Clients.objects.all().delete()
SemenRecords.objects.all().delete()
print("✓ Existing data cleared")

# Create Semen Records
print("\n2. Creating Semen Records...")
semen_records = [
    {'bull_code': 'BULL001', 'bull_name': 'Holstein King', 'bull_breed': 'Holstein', 'num_of_straws': Decimal('50.00'), 'cost_per_straw': Decimal('25.00'), 'company_name': 'Genus ABS'},
    {'bull_code': 'BULL002', 'bull_name': 'Jersey Prime', 'bull_breed': 'Jersey', 'num_of_straws': Decimal('30.00'), 'cost_per_straw': Decimal('30.00'), 'company_name': 'Select Sires'},
    {'bull_code': 'BULL003', 'bull_name': 'Friesian Star', 'bull_breed': 'Friesian', 'num_of_straws': Decimal('40.00'), 'cost_per_straw': Decimal('28.00'), 'company_name': 'URUS'},
]

semen_objects = []
for record in semen_records:
    obj = SemenRecords.objects.create(**record)
    semen_objects.append(obj)
    print(f"  ✓ Created: {obj.bull_code} - {obj.bull_name}")

# Create Cow Records
print("\n3. Creating Cow Records...")
cow_data = [
    {'id': 'COW001', 'name': 'Bessie', 'lactations': 3, 'grade': 'PEDIGREE', 'breed': 'Holstein', 'color': 'Black & White', 'dob': '2019-03-15', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('35.00')},
    {'id': 'COW002', 'name': 'Daisy', 'lactations': 2, 'grade': 'APPENDIX', 'breed': 'Jersey', 'color': 'Brown', 'dob': '2020-05-20', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('30.00')},
    {'id': 'COW003', 'name': 'Buttercup', 'lactations': 4, 'grade': 'FOUNDATION', 'breed': 'Friesian', 'color': 'Black', 'dob': '2018-07-10', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('38.00')},
    {'id': 'COW004', 'name': 'Rosie', 'lactations': 1, 'grade': 'INTERMEDIATE', 'breed': 'Holstein', 'color': 'White & Black', 'dob': '2021-01-25', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('32.00')},
    {'id': 'COW005', 'name': 'Molly', 'lactations': 2, 'grade': 'PEDIGREE', 'breed': 'Jersey', 'color': 'Golden Brown', 'dob': '2020-09-12', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('29.00')},
    {'id': 'COW006', 'name': 'Lily', 'lactations': 0, 'grade': 'POOL', 'breed': 'Holstein', 'color': 'Black & White', 'dob': '2022-11-05', 'status': 'Active', 'category': 'Heifer', 'birth_weight': Decimal('33.00')},
    {'id': 'COW007', 'name': 'Poppy', 'lactations': 3, 'grade': 'FOUNDATION', 'breed': 'Friesian', 'color': 'Black', 'dob': '2019-06-18', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('36.00')},
    {'id': 'COW008', 'name': 'Bella', 'lactations': 1, 'grade': 'APPENDIX', 'breed': 'Jersey', 'color': 'Light Brown', 'dob': '2021-04-30', 'status': 'Active', 'category': 'Milker', 'birth_weight': Decimal('31.00')},
]

cow_objects = []
for data in cow_data:
    data['sire'] = random.choice(semen_objects)
    data['dob'] = datetime.datetime.strptime(data['dob'], '%Y-%m-%d').date()
    obj = Cow.objects.create(**data)
    cow_objects.append(obj)
    print(f"  ✓ Created: {obj.id} - {obj.name} ({obj.breed})")

# Create Client Records
print("\n4. Creating Client Records...")
client_data = [
    {'name': 'Fresh Milk Dairy', 'location': 'Nairobi', 'contacts': '+254712345678', 'unit_price': Decimal('45.00')},
    {'name': 'City Milk Bar', 'location': 'Mombasa', 'contacts': '+254723456789', 'unit_price': Decimal('48.00')},
    {'name': 'Green Valley Store', 'location': 'Kisumu', 'contacts': '+254734567890', 'unit_price': Decimal('42.00')},
    {'name': 'Premium Dairy Shop', 'location': 'Nakuru', 'contacts': '+254745678901', 'unit_price': Decimal('50.00')},
    {'name': 'Morning Fresh Mart', 'location': 'Eldoret', 'contacts': '+254756789012', 'unit_price': Decimal('46.00')},
]

client_objects = []
for data in client_data:
    obj = Clients.objects.create(**data)
    client_objects.append(obj)
    print(f"  ✓ Created: {obj.name} - Ksh {obj.unit_price}/liter")

# Create Milk Production Records (for current month and previous months)
print("\n5. Creating Milk Production Records...")
today = datetime.date.today()
current_year = today.year
current_month = today.month

# Create records for the last 6 months
for months_back in range(6):
    if months_back == 0:
        year = current_year
        month = current_month
    else:
        # Calculate previous months
        month = current_month - months_back
        year = current_year
        while month <= 0:
            month += 12
            year -= 1
    
    # Get number of days in that month
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    last_day = (next_month - datetime.timedelta(days=1)).day
    
    # Create milk production for each day (skip some days randomly)
    for day in range(1, last_day + 1):
        # Skip some days randomly (20% chance)
        if random.random() < 0.2:
            continue
            
        milk_date = datetime.date(year, month, day)
        
        # Create production for each cow
        for cow in cow_objects[:5]:  # Use first 5 cows for daily production
            am_qty = Decimal(str(round(random.uniform(3.0, 8.0), 2)))
            noon_qty = Decimal(str(round(random.uniform(2.0, 5.0), 2)))
            pm_qty = Decimal(str(round(random.uniform(3.0, 7.0), 2)))
            
            # Use get_or_create to avoid unique constraint violations
            obj, created = MilkProductions.objects.get_or_create(
                milk_date=milk_date,
                cow_id=cow,
                defaults={
                    'am_quantity': am_qty,
                    'noon_quantity': noon_qty,
                    'pm_quantity': pm_qty
                }
            )
    
    print(f"  ✓ Created milk production for {month}/{year}")

# Create Milk Sales Records (for current and previous months)
print("\n6. Creating Milk Sales Records...")
for months_back in range(6):
    if months_back == 0:
        year = current_year
        month = current_month
    else:
        month = current_month - months_back
        year = current_year
        while month <= 0:
            month += 12
            year -= 1
    
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    last_day = (next_month - datetime.timedelta(days=1)).day
    
    # Create sales for random days
    for day in range(1, last_day + 1):
        if random.random() < 0.3:  # 30% chance of no sales
            continue
        
        sale_date = datetime.date(year, month, day)
        
        # Create 1-3 sales per day (different clients)
        num_sales = random.randint(1, min(3, len(client_objects)))
        selected_clients = random.sample(client_objects, num_sales)
        
        for client in selected_clients:
            quantity = Decimal(str(round(random.uniform(20.0, 100.0), 2)))
            
            # Use get_or_create to avoid unique constraint violations
            obj, created = MilkSales.objects.get_or_create(
                date=sale_date,
                client=client,
                defaults={
                    'quantity': quantity,
                    'unit_price': client.unit_price
                }
            )
            if created:
                pass  # Successfully created
    
    print(f"  ✓ Created milk sales for {month}/{year}")

# Create Contact Messages
print("\n7. Creating Contact Messages...")
contact_messages = [
    {'name': 'John Smith', 'email': 'john@example.com', 'phone': '+254711111111', 'message': 'I am interested in your dairy management software. Can you provide more information about pricing?', 'is_read': False},
    {'name': 'Sarah Johnson', 'email': 'sarah@farm.com', 'phone': '+254722222222', 'message': 'We have a large dairy farm with 200+ cows. Does your system support bulk operations?', 'is_read': False},
    {'name': 'Michael Brown', 'email': 'michael@dairy.co.ke', 'phone': '+254733333333', 'message': 'Looking for a demo of your milk tracking features. Please contact me.', 'is_read': False},
    {'name': 'Emily Davis', 'email': 'emily@milkfarm.com', 'phone': '', 'message': 'Great product! Would like to integrate with our existing accounting system.', 'is_read': True},
    {'name': 'David Wilson', 'email': 'david@agriculture.org', 'phone': '+254755555555', 'message': 'Can your software handle multiple farm locations?', 'is_read': True},
]

for data in contact_messages:
    obj = ContactMessage.objects.create(**data)
    status = "Unread" if not data['is_read'] else "Read"
    print(f"  ✓ Created: {obj.name} - {status}")

print("\n" + "=" * 60)
print("✓ Database population completed successfully!")
print("=" * 60)
print("\nSummary:")
print(f"  - Cows: {Cow.objects.count()}")
print(f"  - Milk Production Records: {MilkProductions.objects.count()}")
print(f"  - Clients: {Clients.objects.count()}")
print(f"  - Milk Sales Records: {MilkSales.objects.count()}")
print(f"  - Contact Messages: {ContactMessage.objects.count()}")
print(f"  - Semen Records: {SemenRecords.objects.count()}")
print("\nNow you can login and see all data in the admin dashboard!")
print("Login credentials:")
print("  - Admin: admin / admin123")
print("  - Farmer: farmer / farmer123")
print("  - Customer: customer / customer123")
print("=" * 60)
