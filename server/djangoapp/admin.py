from django.contrib import admin

from .models import CarMake, Dealer, Review


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'phone')
    search_fields = ('name', 'city', 'state')


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('make', 'model')
    search_fields = ('make', 'model')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dealer', 'reviewer', 'sentiment', 'created_at')
    search_fields = ('dealer__name', 'reviewer', 'review')
