from django.core.management.base import BaseCommand, CommandError
from newapp.models import Post


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    help = 'накрутить лайки статьям (по 5 штук)'
    # missing_args_message = 'Недостаточно аргументов'
    # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    # requires_migrations_checks = True

    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('argument', nargs='+', type=int)

    # основной код пишется здесь
    def handle(self, *args, **options):
        # функция накрутки лайков статья
        for posts in Post.objects.all():
            posts.rating = posts.rating + 5
            posts.save()
            # выводим сообщение в консоль об успешном выполнении команды
            self.stdout.write(self.style.SUCCESS(f'{posts.id} Успешно добавлены лайки {posts.rating} следующему посту: {posts.title}'))

