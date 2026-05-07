from django.contrib.auth.models import User
from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"


class CarMake(models.Model):
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.make} {self.model}"


class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=80, blank=True)
    car_model = models.CharField(max_length=80, blank=True)
    sentiment = models.CharField(max_length=30, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.dealer.name}"
