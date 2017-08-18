from rest_framework import routers

from api.views import ServiceCategoryViewSet, ProviderViewSet, ServiceViewSet

router = routers.SimpleRouter()
router.register(r'providers', ProviderViewSet, base_name='providers')
router.register(r'categories', ServiceCategoryViewSet, base_name='categories')
router.register(r'services', ServiceViewSet, base_name='services')

urlpatterns = router.urls
