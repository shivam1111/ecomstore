from django.conf.urls import url,include
from ecomstore import settings 
import views as accounts
import django.contrib.auth.views as auth_views

urlpatterns = [
            url(r'^register/$',accounts.register,{'template_name':'registration/register.html', 'SSL': settings.ENABLE_SSL},name = "register"),
            url(r'^my_account/$',accounts.my_account,{'template_name':'registration/my_account.html'},name =  'my_account'),
            url(r'^order_details/(?P<order_id>[-\w]+)/$',accounts.order_details,{'template_name': 'registration/order_details.html'},name='order_details'),
            url(r'^order_info/$',accounts.order_info,{'template_name': 'registration/order_info.html'}, name='order_info')
       ]

urlpatterns.append(
                   url(r'^login/$',auth_views.login,{'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL }, name='login')
                   )