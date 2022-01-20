import instance
from django.http import HttpResponse
from django.views import View

from .tasks import hello, printer, send_mail_for_sub_test


# представление вызова метода hello.delay(), которое выводит сообщение привет
# class IndexView(View):
#     def get(self, request):
#         hello.delay()
#         print("Hello, world! from view!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         return HttpResponse('Hello, проверка таски!')

# class IndexView(View):
#     def get(self, request):
#         hello.delay()
#         printer.delay(10)
#         return HttpResponse('Hello!')

#
class IndexView(View):
    def get(self, request):
        # printer.apply_async([10], countdown=10)
        # hello.delay()
        send_mail_for_sub_test.delay()
        return HttpResponse('Hello!')

# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         printer.apply_async([10])
#         return HttpResponse('Hello!')
