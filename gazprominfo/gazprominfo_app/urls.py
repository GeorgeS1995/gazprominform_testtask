from django.urls import path
from .views import UrlParserApiView, EmailApiView

urlpatterns = [
    path('service1', UrlParserApiView.as_view(), name='service1'),
    path('service2', EmailApiView.as_view(), name='service2'),
]
