from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
        ('broken', 'Требует ремонта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image_url = models.URLField(blank=True, null=True,
                                verbose_name='Ссылка на изображение')
    category = models.CharField(max_length=100, verbose_name='Категория')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES,
                                 verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает рассмотрения'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals',
        on_delete=models.CASCADE, verbose_name='Объявление отправителя')
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals',
        on_delete=models.CASCADE, verbose_name='Объявление получателя')
    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_proposal'
            )
        ]
