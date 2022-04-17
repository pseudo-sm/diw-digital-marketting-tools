import json

from serpapi import GoogleSearch
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import RegUser,EmailAccounts,Business,RateRequest,RealReview
from django.contrib import auth
from django.contrib.auth.models import User
from datetime import datetime
import random
# Create your views here.


def get_user(email):
    regUser = RegUser.objects.get(username=email)
    return regUser

def generate_otp():
    otp = random.randint(100000,999999)
    return otp

def send_email(subject, body, email,doc=None):
    email_msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [email], reply_to=[email])
    if doc is not None:
        email_msg.attach(filename=doc.name,mimetype=doc.content_type,content = doc.read())
    email_msg.send()

def login(request):
    return render(request,"login.html")

def register(request):

    return render(request,"register.html")

def dashboard(request):
    regUser = get_user(request.user.username)
    email_accounts = EmailAccounts.objects.filter(user=regUser)
    business = Business.objects.all()
    return render(request,"dashboard.html",{"email_accounts":email_accounts,"businesses":business})

def rate(request):
    business_id = request.GET.get("business_id")
    email_id = request.GET.get("email_id")
    email = EmailAccounts.objects.get(id=email_id)
    business = Business.objects.get(id=business_id)
    rr = RateRequest(email=email,business=business)
    rr.save()
    return JsonResponse(True,safe=False)

def get_available_email(request):
    business_id = request.GET.get("business_id")
    regUser = get_user(request.user.username)
    email_ids = list(EmailAccounts.objects.filter(user=regUser).values_list("id",flat=True))
    business = Business.objects.get(id=business_id)
    rr = RateRequest.objects.filter(email__in=email_ids,business=business)
    unavailable_email_ids = list(rr.values_list("email",flat=True))
    available_email_ids = [i for i in email_ids if i not in unavailable_email_ids]
    available_emails = list(EmailAccounts.objects.filter(id__in=available_email_ids).values())
    print(available_emails)
    return JsonResponse({"emails":available_emails})

def request_verification(request):
    email = request.GET.get("email")
    otp = generate_otp()
    if len(EmailAccounts.objects.filter(email_id=email)) !=0:
        if len(EmailAccounts.objects.filter(email_id=email,status=True))!=0:
            return JsonResponse(False,safe=False)
        else:
            EmailAccounts.objects.delete(email_id=email)
    regUser = get_user(request.user.username)
    emailAccount = EmailAccounts(email_id=email,otp=otp,user=regUser)
    emailAccount.save()
    send_email("Email Verification","This is your OTP : {}".format(otp),email)
    return JsonResponse(True,safe=False)


def otp_action(request):
    otp = request.GET.get("otp")
    email = request.GET.get("email")
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    email = EmailAccounts.objects.filter(email_id=email).first()
    if int(otp)==int(email.otp):
        email.first_name = first_name
        email.last_name = last_name
        email.status = True
        email.save()
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False,safe=False)

def register_action(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    upi_id = request.POST.get("upi_id")
    reguser = RegUser(upi_id=upi_id,name=name,username=email,password=password)
    reguser.save()
    auth.login(request, reguser)
    return redirect("index")

def login_action(request):
    username = request.POST.get("email")
    password = request.POST.get("password")
    user = auth.authenticate(username=username,password=password)
    auth.login(request,user)
    return redirect("dashboard")

def submit_rate_request(request):
    email_id = request.GET.get("email_id")
    business_id = request.GET.get("business_id")
    email = EmailAccounts.objects.get(id=email_id)
    business = Business.objects.get(id=business_id)
    if list(RateRequest.objects.filter(email=email,business=business)) == []:
        rr = RateRequest(
            email = email,
            business = business
        )
        rr.save()
    return JsonResponse(True,safe=False)

def job(request):

    businesses = Business.objects.all()

    for business in businesses:
        business_id = business.id
        params = {
            "engine": "google_maps",
            "q": business.name,
            "ll": business.location_rule,
            "type": "search",
            "api_key": "486d86ffdedc140f9206882f58f9bd29bc081b1890380ced25679c440db9bea0"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if results.get('place_results') is None:
            data_id = results['local_results'][0]['data_id']
        else:
            data_id = results['place_results']['data_id']
        params = {
            "engine": "google_maps_reviews",
            "data_id": data_id,
            "api_key": "486d86ffdedc140f9206882f58f9bd29bc081b1890380ced25679c440db9bea0"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        reviews = results['reviews']
        for review in reviews:
            name = review["user"]['name']
            text = review["snippet"]
            rating = review['rating']
            date = review['date']
            real_review = RealReview(
                name = name,
                review = text,
                rating = rating,
                date = date,
                business = business
            )
            real_review.save()


    rate_requests = RateRequest.objects.filter(status=False)
    for request in rate_requests:
        time_filters = ['a day ago','2 days ago','3 days ago','hours ago']
        rr = RealReview.objects.filter(business=request.business,date__in=time_filters,name__iexact=request.email.first_name+" "+request.email.last_name,rating='5.0').first()
        print(rr)
        if rr is not None:
            request.status = True
            request.save()
            rr.regUser = request.email.user
            rr.save()
    return JsonResponse({'datetime':datetime.now()})

def report(request):
    rate_request_objects = RateRequest.objects.filter(paid=False,status=True)
    rate_requests = list(rate_request_objects.values("email__first_name","email__user__upi_id","email__email_id","email","id"))
    for i in range(len(rate_requests)):
        rate = rate_requests[i]
        email = rate["email"]
        rate_requests[i]["amount"] = rate_request_objects.filter(email=email).values("id").annotate(total=Count('id')).first()["total"]*5
    return render(request,"report.html",{"rate_requests":rate_requests})

def mark_as_paid(request):
    ids = request.GET.get("ids")
    ids = json.loads(ids)
    RateRequest.objects.filter(id__in=ids).update(paid=True)
    return JsonResponse(True,safe=False)

def logout(request):
    auth.logout(request)
    return redirect("index")