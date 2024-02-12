from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import DealerReview
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
        context = {
            "dealerships": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/index.html', context)
        
# Get Dealer Details View
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url_r = f"https://e1cc25fa-af33-4254-ae3f-56f091075084-bluemix.cloudantnosqldb.appdomain.cloud/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review?dealerId={dealer_id}"
        url_ds = f"https://e1cc25fa-af33-4254-ae3f-56f091075084-bluemix.cloudantnosqldb.appdomain.cloud/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "dealer": get_dealers_from_cf(url_ds)[0],
            "reviews": get_dealer_reviews_from_cf(url_r, dealer_id),
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Add Review View
def add_review(request, dealer_id):
    if request.method == "GET":
        url = f"https://e1cc25fa-af33-4254-ae3f-56f091075084-bluemix.cloudantnosqldb.appdomain.cloud/api/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealers_from_cf(url)[0],
        }
        print(context)
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        form = request.POST
        review = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": form.get("purchasecheck"),
            }
        if form.get("purchasecheck"):
            review["purchasedate"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"]= car.year.strftime("%Y")
        json_payload = {"review": review}
        URL = 'https://e1cc25fa-af33-4254-ae3f-56f091075084-bluemix.cloudantnosqldb.appdomain.cloud/api/review'
        post_request(URL, json_payload, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
