from django.urls import path, include


from .views import IndexView

urlpatterns = [

    # модуль Д7 - таски и редис
    path('', IndexView.as_view(), name='mcd'),


]
