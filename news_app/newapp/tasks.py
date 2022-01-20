from celery import shared_task
from django.core.mail import EmailMultiAlternatives


# таска для отправки писем подписчикам при создании новой
@shared_task
def send_mail_for_sub_test(sub_username, sub_useremail, html_content):
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе!',
        from_email='factoryskill@yandex.ru',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')

    # для удобства вывода инфы в консоль
    print()
    print(html_content)
    print()

    # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
    msg.send()


# таска для отправки писем подписчикам при создании новой
@shared_task
def send_mail_for_sub_test(sub_username, sub_useremail, html_content):
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе!',
        from_email='factoryskill@yandex.ru',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')

    # для удобства вывода инфы в консоль
    print()
    print(html_content)
    print()

    # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
    msg.send()