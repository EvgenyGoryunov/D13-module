from django.urls import path
from django.urls import path

from .views import IndexView
from .views import NewOrderView, take_order

urlpatterns = [

    # модуль Д7 - таски и редис
    path('mcd', IndexView.as_view(), name='mcd'),

    path('', IndexView.as_view()),
    path('new/', NewOrderView.as_view(), name='new_order'),
    path('take/<int:oid>', take_order, name='take_order')

]
