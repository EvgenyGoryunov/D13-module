import instance as instance
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from newapp.models import Category, Post


@shared_task
def send_mail_for_sub(instance):
    print('Сигнал срабатывает 33333333333333333333333')
    print()
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    sub_text = instance.text
    # получаем нужный объект модели Категория через рк Пост
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for qaz in subscribers:
        print(qaz.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print('**********************', subscriber.email, '**********************')
        print(subscriber)
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='factoryskill@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')

        # для удобства вывода инфы в консоль
        print()
        print(html_content)
        print()

        # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
        # msg.send()

    return redirect('/news/')