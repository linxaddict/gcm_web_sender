from django.conf.urls import url

from . import views

app_name = 'gcm_sender'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send/$', views.send_gcm_push, name='send_gcm_push')
]
