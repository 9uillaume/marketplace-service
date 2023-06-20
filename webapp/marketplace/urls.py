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
]
