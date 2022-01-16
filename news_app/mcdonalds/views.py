from django.http import HttpResponse
from django.views import View
from .tasks import hello


# представление вызова метода hello.delay(), которое выводит сообщение привет
class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')