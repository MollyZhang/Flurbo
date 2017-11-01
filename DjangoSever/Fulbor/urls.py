from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/login/', 'Fulbor.views.login', name='login'),
    url(r'^account/signup/', 'Fulbor.views.signup', name='signup'),
]
