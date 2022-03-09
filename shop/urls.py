from django.urls import path
from . import views
urlpatterns = [
   path('',views.index,name= 'index'),
   path('about/',views.about, name='about'),
   path('contact/',views.contact, name='contact'),
   path('tracker/',views.tracker, name='tracker'),
   path('search/',views.search, name='search'),
   path('Product/',views.productPage, name='product'),
   path('productview/<int:prodid>',views.productview , name='productview'),
   path('checkout/',views.checkout , name='checkout'),
   path('privacy/',views.privacy,name='privacy'),
   path("team/", views.team, name="team"),
   path("services/", views.services, name="services"),
   path("handlerequest/", views.handlerequest, name="HandleRequest")

]
