from rest_framework import viewsets, serializers
from service.models import Provider, Service, ServiceCategory


class ProviderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Provider
        fields = ('id', 'name')


class ProviderViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = Provider

    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Service
        fields = ('id', 'name')


class ServiceViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = Service

    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceCategory
        fields = ('id', 'name', 'services')

    services = ServiceSerializer(many=True)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = ServiceCategory

    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
