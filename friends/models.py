from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('self', verbose_name='Друзья', blank=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey('User',
                               verbose_name='Отправитель',
                               on_delete=models.CASCADE,
                               related_name='requests_sent')
    recipient = models.ForeignKey('User',
                                  verbose_name='Получатель',
                                  on_delete=models.CASCADE,
                                  related_name='requests_received')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявка'
