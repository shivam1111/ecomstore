import requests
import base64
import json
from cart.models import CartItem
from cart import cart
from ecomstore import settings
from django.core import urlresolvers
from constance import config
from models import PaypalToken


def _generate_url(url):
    if settings.paypal_sandbox:
        url = ''.join([settings.paypal_sandbox,url])
    else:
        url = ''.join([settings.paypal_live,url])
    
    return url    

def get_token(request):
    endpoint = "/oauth2/token"
    url = _generate_url(endpoint)
    credentials = "%s:%s" % (settings.client_id, settings.client_secret)
    encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")
    headers = {
        "Authorization": ("Basic %s" % encode_credential),
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    param = {
             'grant_type': 'client_credentials',
    }
    r = requests.post(url, headers=headers, data=param)
    response = json.loads(r.text)
    return response.get('access_token',False)

def save_token(payment_id,token):
    token = PaypalToken(payment_id = payment_id,payment_token = token)
    token.save()    
    return True

def create_transactions(request):
    cart_items = cart.get_cart_items(request)
    transactions = []
    total = 0
    description = ''
    for ci in cart_items:
        # create order item for each cart item
        total = total + (ci.price()*ci.quantity)
        description = '|'.join([description,ci.product.name])
    transactions.append({
                        'amount':{
                                  'total':str(total),
                                  "currency":"USD"
                                  },
                        'description':ci.product.name
                        
                        })
    return transactions

def create_paypal_payment(request):
    endpoint = "/payments/payment"
    url = _generate_url(endpoint)
    token = get_token(request)
    host = request.META['HTTP_ORIGIN']
    if token:
        headers = {
            "Authorization": "Bearer %s"%token,
            'Content-Type': 'application/json',
        }
        param = {
                "intent":"sale",
                "redirect_urls":{
                  "return_url":''.join([host,urlresolvers.reverse('execute_payment')]),
                  "cancel_url":''.join([host,urlresolvers.reverse('checkout')]),
                },
                "payer":{
                  "payment_method":"paypal"
                },
#                 "transactions":[
#                   {
#                     "amount":{
#                       "total":"7.47",
#                       "currency":"USD"
#                     },
#                     "description":"This is the payment transaction description."
#                   }
#                 ]
                "transactions":create_transactions(request)
              }
        r = requests.post(url, headers=headers, data=json.dumps(param))
        response = json.loads(r.text)
        save_token(response.get('id',''),token)
        return response
    
def execute_payment(request,getdata):
#     Sample:https://api.sandbox.paypal.com/v1/payments/payment/PAY-6RV70583SB702805EKEYSZ6Y/execute/
    endpoint = "/payments/payment/"
    url = _generate_url(endpoint)
    payment_id = getdata.get('paymentId',[False])
    token = False
    token_record = PaypalToken.objects.get(payment_id = payment_id)
    if token_record:
        token = token_record.payment_token
    if payment_id:
        execue_url = ''.join([url,payment_id,"/execute/"])
        headers = {
            "Authorization": "Bearer %s"%token,
            'Content-Type': 'application/json',
        }
        param = {
                 "payer_id":getdata.get('PayerID',False)
                 }
        r = requests.post(execue_url, headers=headers, data=json.dumps(param))
        # Status 200 if request is successfull
        token_record.delete()
        return r
    
# def execute_mastercard_payment(request):