from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .autor import AutorSerializer
from .livro import LivroSerializer
from .compra import (
    CompraCreateUpdateSerializer,
    CompraListSerializer, # novo
    CompraSerializer,
    ItensCompraCreateUpdateSerializer,
    ItensCompraListSerializer, # novo
    ItensCompraSerializer,
)