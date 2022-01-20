# импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.
import os
from celery import Celery
from celery.schedules import crontab

# связываем настройки Django с настройками Celery через переменную окружения.
# project.settings, project - это имя папки, в которой лежит файл настроек


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации. Мы также указываем
# пространство имен, чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py.
# Он их будет искать по шаблону «CELERY_***».
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
# Строчка звучит дословно - авторазведка боем, в каких проложениях находятся файлы под названием tasks, выхватывать
# от туда все задания, заупаскать их, и помещать в редис
app.autodiscover_tasks()

# для еженедельной рассылки настраиваем расписание запусков таски
app.conf.beat_schedule = {
    'send_mail_every_monday_8am': {
        'task': 'newapp.tasks.send_mail_for_sub_every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}