from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.landing_view, name='landing'),

    path('policy/', views.policy_view, name='policy'),

    path('signup/', views.signup_view, name='signup'),

    path('payment/', views.payment_view, name='payment'),

    path('payment-success/', views.payment_success, name='payment_success'),

    path('login/', views.login_view, name='login'),

    path('home/', views.home_view, name='home'),
]