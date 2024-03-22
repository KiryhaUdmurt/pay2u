from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CategorySerializer,
                             ServiceSerializer,
                             UserSubscriptionSerializer,
                             SubscriptionSerializer)
from .filters import ServiceSearch, SubscriptionFilter
from subscriptions.models import (Category,
                                  Service,
                                  UserSubscription,
                                  Subscription)


class CategoryListRetrieveViewSet(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    """Получает категории списком или по одной."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ServiceListRetrieveViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """Получает сервисы списком или по одному."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (ServiceSearch,)


class SubscriptionListRetrieveViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    """Получает варианты подписок или данные о конкретной подписке."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = (SubscriptionFilter,)

    @action(detail=True, methods=('post',))
    def subscribe(self, request, pk=None):
        subscription = self.get_object()
        user = request.user
        serializer = SubscriptionSerializer(instance=subscription)
        if user.my_subscriptions.filter(subscription=subscription).exists():
            return Response({'error': 'Уже в подписках.'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription.subscribers.create(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSubscriptionViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """Получает подписки пользователя."""
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return UserSubscription.objects.filter(user=user)

    @action(detail=True, methods=('post', 'delete'))
    def renewal(self, request, pk=None):
        user_subscription = self.get_object()
        renewal_status = {'POST': True, 'DELETE': False}
        user_subscription.renewal_status = renewal_status[request.method]
        user_subscription.save()
        serializer = UserSubscriptionSerializer(instance=user_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
