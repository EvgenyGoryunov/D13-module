from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    # cвязь «один к одному» с встроенной моделью пользователей User;
    # когда имеем отношение ко встроенной модели, ее нужно импортировать из джанго
    # from django.contrib.auth.models import User
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    # рейтинг пользователя
    ratingAuthor = models.SmallIntegerField(default=0)

    # метод обновления рейтинга пользователя, суммарный рейтинг пользователя за его посты
    # лайки и прочее
    def update_rating(self):
        # вместо цикла for можно реализовать сбор данных таким образом
        # aggregate, происходит сбор всех данных определенного поля данного пользователя
        # мы суммируем поле 'rating' класс Post
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating', )

        # для комментов суммирование рейтинга, мы суммируем поле 'rating' класс Comment
        # так как "commentPost = models.ForeignKey", в связь добавится "authorUser"
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating', )

        # складываем две переменные, рейтинг за статью (посты), и рейтинг за комменты
        self.ratingAuthor = pRat * 3 + cRat
        # сохранение модели в БД
        self.save()

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.authorUser}'


# Категории новостей/статей — темы, которые они отражают (спорт, политика,образование и т. д.).
class Category(models.Model):
    # Имеет единственное поле: название категории. Поле должно быть уникальным
    # (в определении поля необходимо написать параметр unique = True).
    # максимальную длину строки берут как правило в н-ой степени, 2,4,8,16,32...128,256
    name = models.CharField(max_length=64, unique=True)

    # Модуль Д6
    # Добавляем поле для рассылки пользователям почты по группам подписок
    # связь многие-ко-многим, в нашем случае позволяет формировать список пользователей, относящихся к конкретной
    # категории статьи, то есть в ячейку данных впихать не одно значение (как при других вариантах связи), а сразу
    # целый список, использование связи одна-к-одному, либо одна-ко-многим приводит к тому, что можно
    # выбирать только одного пользователя, а нам нужно много в одной категории статье
    subscribers = models.ManyToManyField(User, )

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.name}'

    # функция абсолютный путь
    # def get_absolute_url(self):
    #     return reverse('news_category', kwargs={'category_id': self.pk})


# Модель статьй и новостей
class Post(models.Model):
    # связь «один ко многим» с моделью Author;
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default="John", verbose_name='Автор')

    # поле с выбором — «статья» или «новость»;
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE,
                                    verbose_name='Категория(categoryType)')

    # автоматически добавляемая дата и время создания;
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default="Nature",
                                 verbose_name='Категория')

    # заголовок статьи/новости;
    title = models.CharField(max_length=128, verbose_name='Название(title)')

    # текст статьи/новости;
    text = models.TextField()

    # рейтинг статьи/новости
    # в данное поле мы сохраняем значение рейтинга, добавляя либо +1(лайк), либо -1 (дизлайк)
    # через методы def like(self) и def dislike(self)
    rating = models.SmallIntegerField(default=0)

    # метод (функция) описания лайков и дизлайков
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # превью статьи, мы взяли часть статьи (первые 123 символа) и прибавили многоточие в конце
    def preview(self):
        return self.text[0:123] + '...'

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


# Под каждой новостью/статьей можно оставлять комментарии, поэтому
# необходимо организовать их способ хранения.
class Comment(models.Model):
    # связь «один ко многим» с моделью Post;
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» с встроенной моделью User (комментарии может оставить любой
    # пользователь, не обязательно автор);
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    # текст комментария;
    text = models.TextField()

    # дата и время создания комментария;
    dateCreation = models.DateTimeField(auto_now_add=True)

    # рейтинг комментария.
    rating = models.SmallIntegerField(default=0)

    # метод (функция) описания лайков и дизлайков
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.commentUser}: {self.text[:20]}'

#
#
#
#
# Осталось с прошлой жизни код, храню на всякий случай

# Промежуточная модель для связи «многие ко многим»:
# class PostCategory(models.Model):

# связь «один ко многим» с моделью Post;
#    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)

# связь «один ко многим» с моделью Category.
#    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
#    postCategory = models.ManyToManyField(Category, through='postCategory')
