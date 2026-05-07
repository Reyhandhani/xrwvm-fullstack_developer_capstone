import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardealership.settings')
django.setup()

from django.contrib.auth.models import User
from djangoapp.models import Dealer, CarMake, Review
import datetime

# Clean up existing
Dealer.objects.all().delete()
CarMake.objects.all().delete()
Review.objects.all().delete()

# Create Root User
if not User.objects.filter(username='root').exists():
    User.objects.create_superuser('root', 'root@example.com', 'admin12345')

# Create Admin User (just in case they still want to use it)
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')

# Create 50 Dealers
states = ['Kansas', 'Texas', 'California', 'New York', 'Florida', 'Ohio', 'Illinois', 'Pennsylvania', 'Georgia', 'Michigan']
for i in range(1, 51):
    state = states[i % len(states)]
    Dealer.objects.create(
        name=f"Auto Dealer {i}",
        city=f"City {i}",
        state=state,
        address=f"{1000 + i} Main St",
        zip_code=f"{10000 + i}",
        phone=f"+1 555 {1000 + i}"
    )

# Create 15 Car Makes
makes_models = [
    ("Toyota", "Camry"), ("Toyota", "Corolla"), ("Toyota", "Rav4"),
    ("Honda", "Civic"), ("Honda", "Accord"), ("Honda", "CR-V"),
    ("Ford", "F-150"), ("Ford", "Mustang"), ("Ford", "Explorer"),
    ("Chevrolet", "Silverado"), ("Chevrolet", "Malibu"), ("Chevrolet", "Equinox"),
    ("Tesla", "Model 3"), ("Tesla", "Model S"), ("Tesla", "Model X")
]

for make, model in makes_models:
    CarMake.objects.create(make=make, model=model)

# Create Reviews for dealer 1
dealer1 = Dealer.objects.first()
Review.objects.create(
    dealer=dealer1, reviewer="bob", review="Good experience and fast service.",
    purchase=True, purchase_date=datetime.date(2026, 1, 15),
    car_make="Honda", car_model="Civic", sentiment="positive"
)
Review.objects.create(
    dealer=dealer1, reviewer="alice", review="Fantastic services. The staff was friendly and helpful.",
    purchase=True, purchase_date=datetime.date(2026, 3, 22),
    car_make="Toyota", car_model="Camry", sentiment="positive"
)

print("Successfully seeded 50 dealers, 15 car models, reviews, and root user.")
