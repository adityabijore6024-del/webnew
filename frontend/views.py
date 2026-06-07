from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
import razorpay
from django.conf import settings


# 1. Landing Page
def landing_view(request):
    return render(request, "landing.html")


# 2. Policy Page
def policy_view(request):
    return render(request, "policy.html")


# 3. Signup Page
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        age = request.POST.get('age')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        request.session['signup_data'] = {
            'username': username,
            'age': age,
            'mobile': mobile,
            'email': email,
            'password': password1
        }

        return redirect('payment')

    return render(request, 'signup.html')


# 4. Payment Page
def payment_view(request):

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": 9900,
        "currency": "INR",
        "payment_capture": 1
    })

    request.session['order_id'] = order['id']

    return render(request, "payment.html", {
        "payment": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


# 5. Payment Success
def payment_success(request):

    data = request.session.get('signup_data')
    order_id = request.session.get('order_id')

    if not data or not order_id:
        return redirect('signup')

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    Profile.objects.create(
        user=user,
        phone=data['mobile'],
        age=data['age']
    )

    request.session.pop('signup_data', None)
    request.session.pop('order_id', None)

    return redirect('login')


# 6. Login
def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username3')
        password = request.POST.get('password3')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 7. Home
def home_view(request):
    return render(request, 'home.html')