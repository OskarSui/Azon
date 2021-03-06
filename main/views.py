from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets
from main.models import Product, Comment
from .serializers import ProductDetailsSerializer, CommentSerializer
from .permissions import ProductPermission, IsCommentAuthor, IsProductAuthor

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'title', 'price']
    search_fields = ['title', ]

    # def get_permissions(self):
    #     """Сюда прилетает какое то действие и если оно равно чтению то ничего не происходит, а если дургое то идет по условию"""
    #     if self.action in ['list', 'retrieve']:
    #         permissions = []
    #     else:
    #         permissions = [ProductPermission, IsProductAuthor, ]
    #     return [permission() for permission in permissions]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProductPermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCommentAuthor, ]
        return [permission() for permission in permissions]