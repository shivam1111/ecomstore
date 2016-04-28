from django.conf.urls import url,include,patterns

urlpatterns = patterns("catalog.views",
           url(r'^$', 'index', { 'template_name':'catalog/index.html'}, 'catalog_home'),
           url(r'^category/(?P<category_slug>[-\w]+)/$','show_category', {'template_name':'catalog/category.html'},'catalog_category'),
           url(r'^product/(?P<product_slug>[-\w]+)/$','show_product', {'template_name':'catalog/product.html'},'catalog_product'),
           url(r'^get_json/','get_json_products'),
           url(r'^review/product/add/$', 'add_review'),
           url(r'^tag/product/add/$', 'add_tag'),
           url(r'^tag_cloud/$', 'tag_cloud', {'template_name': 'catalog/tag_cloud.html'}, 'tag_cloud'),
           url(r'^tag/(?P<tag>[-\w]+)/$', 'tag', {'template_name': 'catalog/tag.html'}, 'tag'),
       )
     
     
