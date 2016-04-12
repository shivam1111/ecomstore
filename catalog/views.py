# encoding=utf8
# this stuff goes at the top of the file, below other imports
from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render_to_response
from catalog.models import Category, Product
from django.template import RequestContext 
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm 

def index(request, template_name="catalog/index.html"):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    # locals() it returns a dictioanary of local variables if you have local variables 
    return render_to_response(template_name, locals(),context_instance = RequestContext(request))

def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description  
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    if request.method == 'POST':
        # add to cart…create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
        #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)  
    else:
        # it’s a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
        # assign the hidden input the product slug
        form.fields['product_slug'].widget.attrs['value'] = product_slug
        # set the test cookie on our first GET request
        request.session.set_test_cookie()
        return render_to_response("catalog/product.html", locals(), context_instance=RequestContext(request)) 
        
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))  