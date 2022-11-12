from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='Окончание URL адреса')
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу',
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe(
                f'<img src={self.image.url} style="width:30px; height:30px"/>'
            )
        else:
            return 'отсутствует'
    image_tag.short_description = 'Картинка'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор блога',
        null=True
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='Подписчик'
            ),
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост с комментариями',
        related_name='comments',
    )
    text = models.TextField(
        help_text='Напишите комментарий',
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[:15]
