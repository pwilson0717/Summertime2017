from django.conf.urls import url
from.import views

app_name = 'pb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^poke$', views.poke, name='poke'),
]