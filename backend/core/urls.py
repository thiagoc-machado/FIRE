from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrokerViewSet, AssetViewSet, OperationViewSet, DashboardViewSet, BackupViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import FireCalculatorView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('brokers', BrokerViewSet)
router.register('assets', AssetViewSet)
router.register('operations', OperationViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'backup', BackupViewSet, basename='backup')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/calculadora-fire/', FireCalculatorView.as_view(), name='calculadora-fire'),
]