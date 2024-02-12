from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm 
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
    context = {}
    # rend if it is a GET req
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # get user info
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            # create new user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

# Get Dealerships View
def get_dealerships(request):
    if request.method == "GET":
        url = "https://maxlp12-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
        
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

