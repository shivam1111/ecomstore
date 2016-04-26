from django.shortcuts import render,render_to_response
import json
from django.template import RequestContext
import paypal_checkout
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from forms import CheckoutForm 
from models import Order, OrderItem
import checkout
from cart import cart
from accounts import profile

def execute_paypal_token(request):
    #Sample URL: http://localhost:8000/cart/?paymentId=PAY-2PX39972HY496933MK4HSDRI&token=EC-41F68379P7654291W&PayerID=DZ233GUZYS6H6
    if request.method  == "GET":
        getdata = request.GET.copy()
        # https://api.sandbox.paypal.com/v1/payments/payment/PAY-6RV70583SB702805EKEYSZ6Y/execute/
        response = paypal_checkout.execute_payment(request,getdata)
        status_code = response.status_code
        response_body = json.loads(response.text)
        receipt_url = urlresolvers.reverse('checkout_receipt')
        return HttpResponseRedirect(receipt_url)
      
def show_checkout(request, template_name='checkout/checkout.html'):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid(): 
            response = checkout.process(request)
            if postdata.get('payment_method',False) == "credit_card":
                order_number = response.get('order_number',0)
                error_message = response.get('message','')   
                if order_number:
                    request.session['order_number'] = order_number
                    receipt_url = urlresolvers.reverse('checkout_receipt')
                    return HttpResponseRedirect(receipt_url)  
            if postdata.get('payment_method',False) == "paypal":
                if response:
                    order_number = response.get('order_number',0)
                    error_message = response.get('message','')   
                    request.session['order_number'] = order_number
                    approval_link = response.get('approval_link',False)
                    return HttpResponseRedirect(approval_link[0].get('href',"."))
                else:
                    pass
        else:
            error_message = 'Correct the errors below'
    else:
        if request.user.is_authenticated(): 
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    page_title = 'Checkout'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request)) 

def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number','')
    if order_number:                           
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
        return render_to_response(template_name,locals(), context_instance=RequestContext(request))
    else:
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url) 