from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="homepage"),
    path("about/",views.about,name="about"),
    path("productview/<int:myid>",views.productview,name="productview"),
    path("search/",views.search,name="search"),
    path("track/",views.track,name="track"),
    path("cart/",views.cart,name="cart"),
    path("check/",views.check,name="check"),
    path("contact/",views.contact,name="contact"),
    path("handlepaytm/",views.handlepaytm,name="handlepaytm")
] 
