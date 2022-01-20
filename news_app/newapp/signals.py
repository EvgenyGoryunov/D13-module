from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор

from .models import Post
from .tasks import send_mail_for_sub


# создаём функцию обработчик с параметрами под регистрацию сигнала
# запускает выполнение кода при каком-либо действии пользователя, в нашем случае -
# создание новой новости и сохранение ее в БД модели Post записи

@receiver(post_save, sender=Post)
# def send_sub_mail(sender, instance, created, **kwargs):
def send_sub_mail(sender, instance, created, **kwargs):
    print('Сигнал срабатывает 111111111111111111111111111')
    send_mail_for_sub(instance)
    print('Сигнал срабатывает 222222222222222222222222222')
