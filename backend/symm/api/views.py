from rest_framework import viewsets, serializers
from service.models import Provider, Service, ServiceCategory


class ProviderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Provider
        fields = ('id', 'name', 'rating')


class ProviderViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = Provider

    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Service
        fields = ('id', 'name', 'price_high', 'price_low', 'duration')


class ServiceDetailSerializer(ServiceSerializer):
    class Meta(object):
        model = Service
        fields = ServiceSerializer.Meta.fields + ('providers',)

    providers = ProviderSerializer(many=True)


class ServiceViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = Service

    serializer_class = ServiceSerializer

    def get_queryset(self):
        qs = Service.objects.all()

        term = self.request.query_params.get('term', '').strip()
        if term:
            qs = qs.filter(name__icontains=term)

        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer

        return ServiceSerializer


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceCategory
        fields = ('id', 'name', 'services')

    services = serializers.SerializerMethodField()

    def get_services(self, cat):
        qs = Service.objects.filter(category=cat)

        term = self.context['request'].query_params.get('term', '').strip()
        if term:
            qs = qs.filter(name__icontains=term)

        return ServiceSerializer(qs, many=True).data


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = ServiceCategory

    serializer_class = ServiceCategorySerializer

    def get_queryset(self):
        qs = ServiceCategory.objects.all()

        term = self.request.query_params.get('term', '').strip()
        if term:
            qs = qs.filter(services__name__icontains=term).distinct()

        return qs
