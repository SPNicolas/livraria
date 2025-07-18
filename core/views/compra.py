from rest_framework.viewsets import ModelViewSet

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
