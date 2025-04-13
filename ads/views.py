from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from .filters import AdFilter, ExchangeProposalFilter
from django_filters.rest_framework import DjangoFilterBackend

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = _('Только автор может выполнять это действие')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def get_object(self):
        try:
            obj = Ad.objects.get(pk=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except Ad.DoesNotExist:
            raise NotFound(detail=_('Объявление не найдено'))


class ExchangeProposalCreateView(generics.CreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad_sender = serializer.validated_data['ad_sender']

        if ad_sender.user != self.request.user:
            raise PermissionDenied(
                _("Вы можете создавать предложения только на свои объявления")
            )

        ad_receiver = serializer.validated_data['ad_receiver']
        if ad_receiver.user == self.request.user:
            raise PermissionDenied(
                _("Нельзя создавать предложения на свои же объявления")
            )

        serializer.save(status='pending')


class ExchangeProposalListView(generics.ListAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExchangeProposalFilter

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        )


class ExchangeProposalUpdateView(generics.UpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            proposal = super().get_object()
            if proposal.ad_receiver.user != self.request.user:
                raise PermissionDenied(
                    _('Только получатель может изменять статус предложения')
                )
            return proposal
        except ExchangeProposal.DoesNotExist:
            raise NotFound(_('Предложение обмена не найдено'))
