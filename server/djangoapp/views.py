from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# About View
def about(request):
    return render(request, 'djangoapp/about.html')

# Contact View
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Login Request View
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'djangoapp/login.html', {'form': form})

# Logout Request View
def logout_request(request):
    logout(request)
    return redirect('/')

# Registration Request View
def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Get Dealerships View
def get_dealerships(request):
    if request.method == "GET":
        url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership"
        # Get dealers from the URL
        context = {
            "dealerships": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/index.html', context)
        
# Get Dealer Details View
def get_dealer_details(request, dealer_id):
    dealer = Dealer.objects.get(pk=dealer_id)
    return render(request, 'djangoapp/dealer_details.html', {'dealer': dealer})

# Add Review View
def add_review(request, dealer_id):
    if request.method == 'POST':
        dealer = Dealer.objects.get(pk=dealer_id)
        review = request.POST['review']
        # Assuming there's a model for reviews related to dealers
        # Create and save the review
        # Redirect to the dealer details page
    else:
        return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id})

