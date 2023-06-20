from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Only allow administrators


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def move_to_new(self, request, pk=None):
        product = self.get_object()
        if product.state == "draft":
            product.move_to_new()
            product.save()
            return Response({"detail": 'Product moved to "new" state.'})

        else:
            return Response(
                {"detail": 'Invalid state for moving to "new".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def reject(self, request, pk=None):
        product = self.get_object()
        if product.state == "new":
            if request.user.is_staff:
                product.reject()
                product.save()

                return Response({"detail": "Product rejected."})
            else:
                return Response(
                    {"detail": "You are not the owner of this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"detail": "Invalid state for rejection."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def ban(self, request, pk=None):
        product = self.get_object()
        if product.state == "new":
            if request.user.is_staff:
                product.ban()
                product.save()
                return Response({"detail": "Product banned."})
            else:
                return Response(
                    {"detail": "You do not have permission to ban this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"detail": "Invalid state for banning."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def accept(self, request, pk=None):
        product = self.get_object()
        if product.state == "new":
            if request.user.is_staff:
                product.accept()
                product.save()
                return Response({"detail": "Product accepted."})
            else:
                return Response(
                    {"detail": "You do not have permission to accept this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"detail": "Invalid state for acceptance."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def move_to_new_from_rejected(self, request, pk=None):
        product = self.get_object()
        if product.state == "rejected":
            if product.is_owner(request.user):
                product.move_to_new_from_rejected()
                product.save()
                return Response({"detail": 'Product moved to "new" state.'})
            else:
                return Response(
                    {
                        "detail": 'You do not have permission to move this product to "new" state.'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"detail": 'Invalid state for moving to "new".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
