from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import action
from core.serializers import CompraSerializer, CompraCreateUpdateSerializer, CompraListSerializer
from core.models import Compra
...
class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.order_by('-id')
    serializer_class = CompraSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CompraListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return CompraCreateUpdateSerializer
        return CompraSerializer
    
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)

    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        compras = Compra.objects.filter(
            status=Compra.StatusCompra.FINALIZADO,
            data__gte=inicio_mes
        )

        total_vendas = sum(compra.total for compra in compras)
        quantidade_vendas = compras.count()

        return Response(
                        {
                                "status": "Relatório de vendas deste mês",
                                "total_vendas": total_vendas,
                                "quantidade_vendas": quantidade_vendas,
                        },
                        status=status.HTTP_200_OK,
                )