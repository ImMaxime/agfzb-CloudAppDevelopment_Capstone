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
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Logout Request View
def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')


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
    return render(request, 'djangoapp/index.html', {'form': form})

# Get Dealerships View
def get_dealerships(request):
    return render(request, 'djangoapp/index.html')
        
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

