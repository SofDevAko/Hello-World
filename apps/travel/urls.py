from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^check$', views.check),
    url(r'^create$', views.create),
    url(r'^travels/$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^travels/addform$', views.addform),
    url(r'^travels/addtravel$', views.addtravel),
    url(r'^travels/join/(?P<id>[0-9]+)$', views.join),
    url(r'^travels/destination/(?P<id>[0-9]+)$', views.show),
]