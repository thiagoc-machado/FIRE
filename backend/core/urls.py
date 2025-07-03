from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrokerViewSet, AssetViewSet, OperationViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('brokers', BrokerViewSet)
router.register('assets', AssetViewSet)
router.register('operations', OperationViewSet)

urlpatterns = router.urls