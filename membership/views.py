from cmd import IDENTCHARS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from requests import request  
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Customer
import stripe
import json
import time
import email 
from SoorajsStore.settings import EMAIL_HOST_USER
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys

stripe.api_key = 'sk_test_51KqHH8SIeyPpwH6UXIU6JXkww9X4NkNqJsgypvtpbgWFPud2v4S3os3WcjgE3lARykc8vVSfkr9mj4TW458VYYV30094N3JEMN'

# stripe.Invoice.send_invoice("A7689D29-0001")
# CUSTOMER = [{email = 'soorajkpkrishna45@!gmail.com' , stripe_id =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)}]


# def send_invoice(request):
 
#   stripe.InvoiceItem.create(
#   customer='cus_LdCxBab9frC8C9',
#   price='price_1Ky8BVSIeyPpwH6UnOlGhKym',
# ) 
#   stripe.Invoice.send_invoice()
#   return HttpResponse("Send succeffully")
        


#   return render (request,'exit.html')
 


CUSTOMERS = [{"stripe_id": "cus_Lf85DIAH2d0Igk" , "email":" dracupubg@gmail.com "}]
# # Prices in Stripe model the pricing scheme of your business.
# # Create Prices in the Dashboard or with the API before accepting payments
# # and store the IDs in your database.
PRICES = {"basic": "price_1KussASIeyPpwH6UTv79O3AP", "professional": "price_1KxPdeSIeyPpwH6UoO6fz7QU"}

def send_invoice(email):
   
  # Look up a customer in your database
    customers = [c for c in CUSTOMERS if c["email"] == email]
   
    customer_id= customers[0]["stripe_id"]
    stripe.Invoice.send_invoice("in_1KxOkCSIeyPpwH6UpZSds7u4")
    return HttpResponse("Send succeffully")
        
    # else:
    #     # Create a new Customer
    #         customer = stripe.Customer.create(
    #         email= "dracupubg@gmail.com", # Use your email address for testing purposes
    #         description="Customer to invoice",
    #     )
    #     # Store the customer ID in your database for future purchases
    #     CUSTOMERS.append({"stripe_id": customer.id, "email": email})
    #     # Read the Customer ID from your database
        # customer_id = customer.id

    # Create an Invoice Item with the Price and Customer you want to charge
    # stripe.InvoiceItem.create( # You can create an invoice item after the invoice
    #     customer=customer_id,
    #     price=PRICES["basic"],
    # )

    # # Create an Invoice
    
    # invoice = stripe.Invoice.create(
    
    # collection_method='send_invoice',
    
    # days_until_due=30,
    # customer=customer_id,
    # )
    #     # Send the Invoice
    # stripe.Invoice.send_invoice(invoice.id)
    # return HttpResponse("Send succeffully")
        
      


def delete(request):
  stripe.Subscription.delete(stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id))
  return HttpResponse("Cancelled succeffully")

#use this working updartion view
def modify(request):
 if request.method == 'GET' :
    subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='create_prorations',
    items=[{
        'id': subscription['items']['data'][0].id,
    
        'price': 'price_1KxPdeSIeyPpwH6UoO6fz7QU',
    
    }]
    )
    return render(request,'exit.html')

def downgrade(request):
 if request.method == 'GET' :
    subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='create_prorations',
    items=[{
        'id': subscription['items']['data'][0].id,
    
        'price': 'price_1KussASIeyPpwH6UTv79O3AP',
    
    }]
    )
    return render(request,'exit.html')


def upgrade(request):
    subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='create_prorations',
    items=[{
        'id': subscription['items']['data'][0].id,
        'price': 'price_1KussASIeyPpwH6UTv79O3AP',

    }]
    )

def pausepayments(request):
    customer_id= stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id),
    stripe.Subscription.modify(
    request.user.customer.stripe_subscription_id,
    pause_collection={
        'behavior': 'mark_uncollectible',
   
    },
    )
    return HttpResponse("Successfully Paused")

def unpause(request):

        stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection='',
        )
        return render(request,  "exit.html")

def index(request):
    return HttpResponse("Welcome to our Membership website")

def home(request):
    return render(request, 'home.html')


@login_required
def settings(request):
    return render(request, 'settings.html')


def join(request):
    return render(request, 'join.html')

def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 18
        membership_id = 'price_1KussASIeyPpwH6UTv79O3AP'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1KussASIeyPpwH6UTv79O3AP'
                final_dollar = 1800

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})


class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

@login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})

@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')