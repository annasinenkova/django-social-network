from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    caption = models.TextField(blank=True, verbose_name='Подпись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes = models.IntegerField(blank=True, default=0)
    comm = models.IntegerField(blank=True, default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.caption


class Comments(models.Model):
    content = models.TextField(blank=True, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Автор')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True, verbose_name='Под постом')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, verbose_name='Текст')
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(default='default.png', upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
