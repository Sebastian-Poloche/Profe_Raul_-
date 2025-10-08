from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from projects.views import ProductoViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProductoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
