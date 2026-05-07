import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardealership.settings')

import django
django.setup()

from django.contrib.auth.models import User
from djangoapp.models import CarMake, Dealer, Review


Dealer.objects.all().delete()
CarMake.objects.all().delete()
Review.objects.all().delete()

dealers = [
    {
        'name': 'Kansas City Best Cars',
        'city': 'Kansas City',
        'state': 'Kansas',
        'address': '100 Main Street',
        'zip_code': '66101',
        'phone': '+1 913 555 1000',
    },
    {
        'name': 'Wichita Auto Center',
        'city': 'Wichita',
        'state': 'Kansas',
        'address': '220 Market Road',
        'zip_code': '67202',
        'phone': '+1 316 555 2200',
    },
    {
        'name': 'California Auto Hub',
        'city': 'Los Angeles',
        'state': 'California',
        'address': '88 Sunset Boulevard',
        'zip_code': '90001',
        'phone': '+1 213 555 8800',
    },
    {
        'name': 'New York Premium Cars',
        'city': 'New York',
        'state': 'New York',
        'address': '45 Madison Avenue',
        'zip_code': '10010',
        'phone': '+1 212 555 4500',
    },
    {
        'name': 'Texas Family Motors',
        'city': 'Dallas',
        'state': 'Texas',
        'address': '300 Elm Street',
        'zip_code': '75201',
        'phone': '+1 214 555 3000',
    },
]

created_dealers = []

for dealer_data in dealers:
    created_dealers.append(Dealer.objects.create(**dealer_data))

cars = [
    ('Toyota', 'Camry'),
    ('Toyota', 'Corolla'),
    ('Honda', 'Civic'),
    ('Honda', 'Accord'),
    ('Ford', 'F-150'),
    ('Chevrolet', 'Malibu'),
    ('Tesla', 'Model 3'),
]

for make, model in cars:
    CarMake.objects.create(make=make, model=model)

Review.objects.create(
    dealer=created_dealers[0],
    reviewer='alice',
    review='Fantastic services. The staff was friendly and helpful.',
    purchase=True,
    car_make='Toyota',
    car_model='Camry',
    sentiment='positive',
)

Review.objects.create(
    dealer=created_dealers[0],
    reviewer='bob',
    review='Good experience and fast service.',
    purchase=False,
    car_make='Honda',
    car_model='Civic',
    sentiment='positive',
)

Review.objects.create(
    dealer=created_dealers[1],
    reviewer='charlie',
    review='The waiting time was slow but the staff was polite.',
    purchase=True,
    car_make='Ford',
    car_model='F-150',
    sentiment='negative',
)

print('Seed data created successfully.')
