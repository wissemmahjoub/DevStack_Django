from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accueil$', views.home),
    url(r'^date$', views.date_actuelle),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
    url(r'^upload/$', views.simple_upload, name='upload'),
    url(r'^token$', views.token),
    url(r'^createImg/$', views.createImg, name='createImg'),
    url(r'^addvolume$', views.addvolume , name='addvolume'),
    url(r'^listevolume/$', views.listevolume, name='listevolume')

]