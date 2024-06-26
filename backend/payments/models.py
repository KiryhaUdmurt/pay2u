from django.db import models
from django.utils import timezone

from subscriptions.models import UserSubscription
from users.models import User


class Payment(models.Model):
    """Оплата подписки."""
    amount = models.PositiveIntegerField('Сумма')
    cashback = models.PositiveIntegerField('Сумма кешбэка')
    cashback_status = models.BooleanField(
        'Статус начислнения кешбэка',
        default=False)
    date = models.DateTimeField('Дата оплаты', default=timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_payments',
        verbose_name='Пользователь')
    user_subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_payments',
        verbose_name='Подписка пользователя')

    def save(self, *args, **kwargs):
        self.cashback = (
            self.amount * self.user_subscription.subscription.cashback) / 100
        super().save(*args, **kwargs)
