from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.main),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^addQuote$', views.addQuote),
	url(r'^addFavorites/(?P<id>\d+)$', views.addFavorites),
	url(r'^removeFavorites/(?P<id>\d+)$', views.removeFavorites),
	url(r'^users/(?P<id>\d+)$', views.userPosts),
]