from django.conf.urls import url,include,patterns
from ecomstore import settings 

urlpatterns = patterns('checkout.views',
                       (r'^execute_payment/', 'execute_paypal_token',{},'execute_payment'),
                       (r'^$', 'show_checkout', {'template_name': 'checkout/checkout.html', 'SSL': settings.ENABLE_SSL }, 'checkout'),
                       (r'^receipt/$', 'receipt', {'template_name': 'checkout/receipt.html','SSL': settings.ENABLE_SSL },'checkout_receipt'),
) 