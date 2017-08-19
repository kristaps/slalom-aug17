from rest_framework import routers

from api.views import ServiceCategoryViewSet, ProviderViewSet, ServiceViewSet, AppointmentViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'providers', ProviderViewSet, base_name='providers')
router.register(r'categories', ServiceCategoryViewSet, base_name='categories')
router.register(r'services', ServiceViewSet, base_name='services')
router.register(r'appointments', AppointmentViewSet, base_name='appointments')

urlpatterns = router.urls
