from cart import cart
from models import Order, OrderItem
from forms import CheckoutForm
import authnet
from ecomstore import settings
from django.core import urlresolvers
import urllib
import paypal_checkout

# returns the URL from the checkout module for cart
def get_checkout_url(request):
    return urlresolvers.reverse('checkout')

def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    results = {}
    postdata = request.POST.copy()
    if postdata.get('payment_method',False) == "credit_card":
        card_num = postdata.get('credit_card_number','')
        exp_month = postdata.get('credit_card_expire_month','')
        exp_year = postdata.get('credit_card_expire_year','')
        exp_date = exp_month + exp_year
        cvv = postdata.get('credit_card_cvv','')
        amount = cart.cart_subtotal(request)
        
        response = authnet.do_auth_capture(amount=amount,card_num=card_num,exp_date=exp_date,card_cvv=cvv)  
        if response[0] == APPROVED:
            transaction_id = response[6]
            order = create_order(request, transaction_id)
            results = {'order_number':order.id,'message':''}
    if postdata.get('payment_method',False) == "paypal":
        response = paypal_checkout.create_paypal_payment(request)
        if response.get('id',False): # This means the transaction was approved
            order = create_order(request, response.get('id'))
            results = {'order_number':order.id,'message':''}
            links = response.get("links",False)
            if links: 
                approval_link = filter(lambda link: link['rel'] == 'approval_url', links)
                results = {'order_number':order.id,'message':'','approval_link':approval_link}
        else:
            return False
    return results

def create_order(request,transaction_id):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id 
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.status = Order.SUBMITTED
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user 
    order.save()
    
    # if the order save succeeded 
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price() # now using @property
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)
        # save profile info for future orders
    if request.user.is_authenticated():
        from accounts import profile
        profile.set(request)
    # return the new order object
    return order    
     
