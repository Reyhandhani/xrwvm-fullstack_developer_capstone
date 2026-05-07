from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dealers/state/<str:state>/', views.dealers_by_state_page, name='dealers_by_state_page'),
    path('dealer/<int:dealer_id>/', views.dealer_detail_page, name='dealer_detail_page'),
    path('dealer/<int:dealer_id>/review/', views.add_review_page, name='add_review_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name='register_page'),

    path('djangoapp/login', views.api_login, name='api_login'),
    path('djangoapp/logout', views.api_logout, name='api_logout'),
    path('djangoapp/register', views.api_register, name='api_register'),
    path('djangoapp/get_dealers/', views.api_get_dealers, name='api_get_dealers'),
    path('djangoapp/get_dealers/<str:state>', views.api_get_dealers_by_state, name='api_get_dealers_by_state'),
    path('djangoapp/dealer/<int:dealer_id>', views.api_get_dealer_by_id, name='api_get_dealer_by_id'),
    path('djangoapp/reviews/dealer/<int:dealer_id>', views.api_get_reviews_by_dealer, name='api_get_reviews_by_dealer'),
    path('djangoapp/get_cars', views.api_get_cars, name='api_get_cars'),
    path('djangoapp/analyze/<path:text>', views.api_analyze_review, name='api_analyze_review'),
]
