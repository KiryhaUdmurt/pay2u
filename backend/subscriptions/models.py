from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import User


class Service(models.Model):
    """Сервис подписок."""
    name = models.CharField('Сервис', max_length=200, unique=True,
                            db_index=True)
    description = models.TextField('Описание cервиса')
    color = models.CharField(
        'Цвет',
        validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{6})$')])
    image = models.ImageField('Лого сервиса', upload_to='services/')
    image_card = models.ImageField(
        'Карточка сервиса',
        upload_to='services_cards/')
    created = models.DateTimeField('Дата создания', default=timezone.now)
    rating = models.PositiveIntegerField(
        'Рейтинг сервиса',
        default=settings.MIN_RATING,
        validators=[MinValueValidator(settings.MIN_RATING),
                    MaxValueValidator(settings.MAX_RATING)])
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Категория')


class Category(models.Model):
    """Категория подписок."""
    name = models.CharField('Категория', max_length=200, unique=True)
    description = models.TextField('Описание категории')
    image = models.ImageField('Лого категории', upload_to='categories/')


class Subscription(models.Model):
    """Вариант подписки на сервис."""
    name = models.CharField('Подписка', max_length=200)
    description = models.TextField('Описание подписки')
    price = models.PositiveIntegerField('Стоимость')
    months = models.PositiveIntegerField(
        'Период действия в месяцах',
        default=settings.MIN_MONTHS,
        validators=[MinValueValidator(settings.MIN_MONTHS),
                    MaxValueValidator(settings.MAX_MONTHS)])
    cashback = models.PositiveIntegerField(
        'Кешбэк подписки',
        default=settings.MIN_CASHBACK,
        validators=[MinValueValidator(settings.MIN_CASHBACK),
                    MaxValueValidator(settings.MAX_CASHBACK)])
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Сервис')


class Favorite(models.Model):
    """Избранные сервисы пользователей."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь')
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Сервис')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'service'),
                                    name='unique_user_service')
        ]


class UserSubscription(models.Model):
    """Подписки пользователя."""
    start_date = models.DateTimeField('Дата начала', default=timezone.now)
    end_date = models.DateTimeField('Дата окончания')
    status = models.BooleanField('Статус', default=True)
    renewal_status = models.BooleanField('Статус автопродления', default=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_subscriptions',
        verbose_name='Пользователь')
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписка')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'subscription'),
                                    name='unique_user_subscription')
        ]

    def save(self, *args, **kwargs):
        """Вычисление даты окончания подписки."""
        self.end_date = self.start_date + relativedelta(
            months=self.subscription.months)
        super().save(*args, **kwargs)


@receiver(post_save, sender=UserSubscription)
def create_payment(sender, instance, created, **kwargs):
    """
    Создает платеж, после создания объекта UserSubscription.
    Привязывает свободный промокод пользователю.
    """
    if created:
        instance.user_payments.create(
            amount=instance.subscription.price,
            date=instance.start_date,
            user=instance.user)
        promocodes = instance.subscription.promo_codes.filter(
            usage_status=False)
        if promocodes.exists():
            promocode = promocodes.first()
            promocode.start_date = timezone.now()
            promocode.user = instance.user
            promocode.usage_status = True
            promocode.save()


class PromoCode(models.Model):
    """Промокоды сервисов для активации подписок
    на устройствах пользователей."""
    code = models.CharField('Промокод', max_length=20)
    start_date = models.DateTimeField(
        'Дата создания',
        null=True,
        blank=True)
    end_date = models.DateTimeField('Дата истечения')
    usage_status = models.BooleanField('Статус использования', default=False)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='promo_codes',
        verbose_name='Подписка')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='promo_codes',
        verbose_name='Подписка',
        null=True,
        blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('code', 'subscription'),
                                    name='unique_code_subscription')
        ]
