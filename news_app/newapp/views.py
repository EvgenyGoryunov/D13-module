from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin  # модуль Д5, чтоб ограничить права доступа
from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Category

# from mcdonalds.tasks import hello
#
#
# def index(request):
#     hello.delay()
#     return render(request, 'news_list.html')


# дженерик для главной страницы
class NewsList(ListView):
    model = Post  # (2)
    template_name = 'news_list.html'
    context_object_name = 'posts'  # (3)
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст, то есть чтоб переменная 'filter' появилась на странице
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для поиска статей
class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст странички
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для получения деталей о посте
class NewsDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

    # для отображения кнопок подписки (если не подписан: кнопка подписки - видима, и наоборот)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
        id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Пост)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        qwe = Category.objects.filter(pk=Post.objects.get(pk=id).category.id).values("subscribers__username")
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not qwe.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = qwe.filter(subscribers__username=self.request.user).exists()
        return context


# дженерик для создания объекта. Можно указать только имя шаблона и класс формы
class NewsAdd(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    success_url = '/news/'


# (0)


# дженерик для редактирования объекта
class NewsEdit(UpdateView):
    template_name = 'news_edit.html'
    form_class = NewsForm
    success_url = '/news/'  # после редактирования статьи перейдем по указанному адресу (на главную)

    def get_object(self, **kwargs):  # (4)
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class NewsDelete(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'  # после удаления нашей статьи перейдем по указанному адресу


# (5)
@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')


# Модуль Д5 - Ограничения прав доступа
# (1)
class AddNews(PermissionRequiredMixin, NewsAdd):
    permission_required = ('newapp.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsEdit):
    permission_required = ('newapp.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDelete):
    permission_required = ('newapp.delete_post',)
#
#
#
#
#
# (7)
# способ отправки писем с разным содержимым, то есть по мимо текста можно отправить например
# готовую страницу html (шаблон с готовым содержимым как в нашем случае)
#
# (6)
# все что касается отправки писем в Django читать здесь
# https://www.djbook.ru/rel3.0/topics/email.html#mail-admins
# Отправка письма с шаблоном внутри
# Здесь указываем имя нашего шаблона, и что будет в нашем шаблона, то есть передаем все наши переменные
# и их значения в наш шаблон, если не указать явно их, то будут пустые строчки
#
# (5)
# функция подписки пользователя на категорию новости, которую в данный момент читает пользователь
# передаем с нашей странички news_detail.html на которой находится пользователь (представление DetailView)
# через GET запрос информацию в виде значения переменной ?pk={{ post.category.id }}, далее из объекта request
# через метод GET.get('pk') выдираем ее значение (число) и используем для поиска в модели категории нужной
# категории. С помощью метода add(request.user) добавляем нового пользователя в поле подписоты subscribers на
# рассылку, добавляется связь многие-ко-многим в промежуточной таблице category_subscribers
# (содержит ид записи, ид категории, ид юзера)
#
# (4)
# метод get_object используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
#
# (3)
# это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку
# объектов через HTML-шаблон
#
# (2)
# указываем модель, объекты которой мы будем выводить
# указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно
# пользователю должны вывестись наши объекты
#
# (1)
# через запятую указываем какие права хотим ограничить, предварительно в админ панели создали необходимые ограничения,
# а в данном месте мы накладываем ограничения конкретно на представление, то есть выводы страничек сайта, если
# пользователь не входит в нужную группу, ему вылетает страница с ошибкой 403 (страница недоступна вам)
# Существует определенное соглашение для именования разрешений: <app>.<action>_<model>, пример 'newapp.add_post'
# После того, как мы написали наши ограничения, нужно в urls изменить выводы преставлений, указав на новые
#
# (0)
# Первый способ отправки сообщений подписчику (второй через сигналы сделан)
# def post(self, request, *args, **kwargs):
#     form = NewsForm(request.POST)
#     # category_pk = request.POST['category'] # либо так можно, либо как ниже
#     category_pk = request.POST.get('category')
#     sub_text = request.POST.get('text')
#     sub_title = request.POST.get('title')
#     category = Category.objects.get(pk=category_pk)
#     subscribers = category.subscribers.all()
#     # получаем адрес хоста и порта (в нашем случае 127.0.0.1:8000), чтоб в дальнейшем указать его в ссылке
#     # в письме, чтоб пользователь мог с письма переходить на наш сайт, на конкретную новость
#     host = request.META.get('HTTP_HOST')
#
#
#     # валидатор - чтоб данные в форме были корректно введены, без вредоносного кода от хакеров и прочего
#     if form.is_valid():
#         news = form.save(commit=False)
#         news.save()
#         print('Статья:', news)
#
#     for subscriber in subscribers:
#         # print('Адреса рассылки:', subscriber.email)
#
#         # (6)
#         html_content = render_to_string(
#             'mail_sender.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'host': host})
#
#         # (7)
#         msg = EmailMultiAlternatives(
#             # Заголовок письма, тема письма
#             subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
#             # Наполнение письма
#             body=f'{sub_text[:50]}',
#             # От кого письмо (должно совпадать с реальным адресом почты)
#             from_email='factoryskill@yandex.ru',
#             # Кому отправлять, конкретные адреса рассылки, берем из переменной, либо можно явно прописать
#             to=[subscriber.email],
#         )
#
#         msg.attach_alternative(html_content, "text/html")
#         print(html_content)
#         msg.send()
#
# return redirect('/news/')
