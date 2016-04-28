from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def catalog(request):
    site_name = "J & G Infosystems"
    response_html =  u"<html><body>Welcome to %s.</body></html>" % site_name
    return HttpResponse(response_html) 

def file_not_found_404(request):
    page_title = 'Page Not Found'
    return render_to_response('404.html', locals(),context_instance=RequestContext(request))