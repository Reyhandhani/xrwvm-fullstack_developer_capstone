import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, Dealer, Review


def analyze_text(text):
    positive_words = ['good', 'great', 'fantastic', 'excellent', 'amazing', 'best', 'helpful', 'friendly']
    negative_words = ['bad', 'poor', 'terrible', 'worst', 'slow', 'rude', 'awful']

    clean_text = text.lower()

    if any(word in clean_text for word in positive_words):
        return 'positive'

    if any(word in clean_text for word in negative_words):
        return 'negative'

    return 'neutral'


def home(request):
    dealers = Dealer.objects.all().order_by('id')
    states = Dealer.objects.values_list('state', flat=True).distinct().order_by('state')

    context = {
        'dealers': dealers,
        'states': states,
    }

    return render(request, 'djangoapp/home.html', context)


def dealers_by_state_page(request, state):
    dealers = Dealer.objects.filter(state__iexact=state).order_by('id')
    states = Dealer.objects.values_list('state', flat=True).distinct().order_by('state')

    context = {
        'dealers': dealers,
        'states': states,
        'selected_state': state,
    }

    return render(request, 'djangoapp/home.html', context)


def dealer_detail_page(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = Review.objects.filter(dealer=dealer).order_by('-created_at')

    context = {
        'dealer': dealer,
        'reviews': reviews,
    }

    return render(request, 'djangoapp/dealer_detail.html', context)


@login_required
def add_review_page(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    car_makes = CarMake.objects.all().order_by('make')

    if request.method == 'POST':
        review_text = request.POST.get('review', '')
        purchase = request.POST.get('purchase') == 'on'

        Review.objects.create(
            dealer=dealer,
            reviewer=request.user.username,
            review=review_text,
            purchase=purchase,
            purchase_date=request.POST.get('purchase_date') or None,
            car_make=request.POST.get('car_make', ''),
            car_model=request.POST.get('car_model', ''),
            sentiment=analyze_text(review_text),
        )

        return redirect('dealer_detail_page', dealer_id=dealer.id)

    context = {
        'dealer': dealer,
        'car_makes': car_makes,
    }

    return render(request, 'djangoapp/add_review.html', context)


def login_page(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        error_message = 'Invalid username or password.'

    return render(request, 'djangoapp/login.html', {'error_message': error_message})


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists.'
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            login(request, user)
            return redirect('home')

    return render(request, 'djangoapp/register.html', {'error_message': error_message})


def dealer_to_dict(dealer):
    return {
        'id': dealer.id,
        'full_name': dealer.name,
        'short_name': dealer.name,
        'city': dealer.city,
        'state': dealer.state,
        'address': dealer.address,
        'zip': dealer.zip_code,
        'phone': dealer.phone,
        'latitude': 0.0,
        'longitude': 0.0,
    }


def review_to_dict(review):
    return {
        'id': review.id,
        'dealer': review.dealer.id,
        'reviewer': review.reviewer,
        'review': review.review,
        'purchase': review.purchase,
        'purchase_date': str(review.purchase_date) if review.purchase_date else '',
        'car_make': review.car_make,
        'car_model': review.car_model,
        'sentiment': review.sentiment,
    }


@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        data = request.POST

    username = data.get('userName') or data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'Authenticated', 'userName': user.username})

    return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)


def api_logout(request):
    logout(request)
    return JsonResponse({'userName': ''})


@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        data = request.POST

    username = data.get('userName') or data.get('username')
    first_name = data.get('firstName') or data.get('first_name')
    last_name = data.get('lastName') or data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    return JsonResponse({'status': 'success', 'message': 'User registered', 'userName': user.username})


def api_get_dealers(request):
    dealers = Dealer.objects.all().order_by('id')
    return JsonResponse({'dealers': [dealer_to_dict(dealer) for dealer in dealers]})


def api_get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state).order_by('id')
    return JsonResponse({'dealers': [dealer_to_dict(dealer) for dealer in dealers]})


def api_get_dealer_by_id(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    return JsonResponse({'dealer': dealer_to_dict(dealer)})


def api_get_reviews_by_dealer(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = Review.objects.filter(dealer=dealer).order_by('-created_at')
    return JsonResponse([review_to_dict(review) for review in reviews], safe=False)


def api_get_cars(request):
    cars = CarMake.objects.all().order_by('make')
    data = [{'make': car.make, 'model': car.model} for car in cars]
    return JsonResponse({'CarModels': data})


def api_analyze_review(request, text):
    sentiment = analyze_text(text)
    return JsonResponse({'review': text, 'sentiment': sentiment})
