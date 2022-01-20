from django.urls import path
from django.urls import path

from .views import IndexView


urlpatterns = [

    # модуль Д7 - таски и редис
    path('mcd/', IndexView.as_view(), name='mcd'),

    # path('', IndexView.as_view()),


]
