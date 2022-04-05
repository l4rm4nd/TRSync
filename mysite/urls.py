from django.conf.urls import url
from django.urls import path, include # new
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include 
from polls.views import *
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
  path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
  path('', index, name='index'),
  path(r'index/', index, name="index"),
  path(r'api/login/', login, name="login"),
  #path(r'admin/', admin.site.urls),
  path(r'api/download/', download, name="download"),
  path(r'session_security/', include('session_security.urls')),

]

handler404 = 'polls.views.error_404'
handler500 = 'polls.views.error_500'
handler403 = 'polls.views.error_403'