from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiExample

from core.models import Livro
from core.serializers import (
    LivroAlterarPrecoSerializer,
    LivroRetrieveSerializer,
    LivroListSerializer,
    LivroSerializer,
    LivroAjustarEstoqueSerializer
)

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    @action(detail=True, methods=['patch'])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data['preco']
        livro.save()

        return Response(
            {'detail': f'Preço do livro "{livro.titulo}" atualizado para {livro.preco}.'}, status=status.HTTP_200_OK
        )
    
    @extend_schema(
        summary="Ajusta o estoque de um livro",
        description="Aumenta ou diminui o estoque; impede resultado negativo.",
        request=LivroAjustarEstoqueSerializer,
        responses={
            200: OpenApiExample(
                'Estoque ajustado',
                value={'status': 'Quantidade ajustada com sucesso', 'novo_estoque': 30},
                response_only=True,
            ),
            400: OpenApiExample(
                'Erro de validação',
                value={'quantidade': ['A quantidade em estoque não pode ser negativa.']},
                response_only=True,
            ),
        }
    )
    @action(detail=True, methods=['post'])
    def ajustar_estoque(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAjustarEstoqueSerializer(data=request.data, context={'livro': livro})
        serializer.is_valid(raise_exception=True)

        quantidade_ajuste = serializer.validated_data['quantidade']
        livro.quantidade += quantidade_ajuste
        livro.save()
        
        return Response(
            {'status': 'Quantidade ajustada com sucesso', 'novo_estoque': livro.quantidade},
            status=status.HTTP_200_OK
        )
