from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers, permissions
from item.views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("", TemplateView.as_view(template_name="default_urlconf.html")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/categories/",
        CategoryViewSet.as_view({"post": "create"}),
        name="category-create",
        kwargs={"permission_classes": [permissions.IsAdminUser]},
    ),
    path(
        "api/categories/",
        CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "api/categories/<int:pk>/",
        CategoryViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="category-detail",
    ),
    path(
        "api/products/",
        ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product-list",
    ),
    path(
        "api/products/accepted",
        ProductViewSet.as_view({"get": "accepted"}),
        name="product-accepted",
    ),
    path(
        "api/products/<int:pk>/",
        ProductViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="product-detail",
    ),
    path(
        "api/products/<int:pk>/reject/",
        ProductViewSet.as_view({"post": "reject"}),
        name="product-reject",
    ),
    path(
        "api/products/<int:pk>/ban/",
        ProductViewSet.as_view({"post": "ban"}),
        name="product-ban",
    ),
    path(
        "api/products/<int:pk>/accept/",
        ProductViewSet.as_view({"post": "accept"}),
        name="product-accept",
    ),
    path(
        "api/products/<int:pk>/move-to-new/",
        ProductViewSet.as_view({"post": "move_to_new"}),
        name="product-move-to-new",
    ),
    path(
        "api/products/<int:pk>/move-to-new-from-rejected/",
        ProductViewSet.as_view({"post": "move_to_new_from_rejected"}),
        name="product-move-to-new-from-rejected",
    ),
]
