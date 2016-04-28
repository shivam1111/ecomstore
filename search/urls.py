from django.conf.urls import url,include,patterns 
import views

urlpatterns =[
              url(r'^results/$',views.results,{'template_name': 'search/results.html'}, 'search_results'),
              ] 


