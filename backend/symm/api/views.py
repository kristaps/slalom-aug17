from collections import defaultdict
from datetime import timedelta, datetime, date

from rest_framework import viewsets, serializers, decorators, response
from rest_framework.generics import get_object_or_404

from service.models import Provider, Service, ServiceCategory, Appointment
from dateutil.parser import parse as dateutil_parse
from dateutil.rrule import rrule, DAILY, HOURLY, MO, TU, WE, TH, FR, SU
from dateutil.relativedelta import relativedelta


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

    @decorators.detail_route(methods=['GET'])
    def availability_a(self, request, pk):
        service = get_object_or_404(Service.objects.filter(pk=pk))

        date_from = self.request.query_params.get('date_from', '').strip()
        date_to = self.request.query_params.get('date_to', '').strip()

        if date_from:
            date_from = dateutil_parse(date_from)
        else:
            date_from = date.today() + timedelta(days=1)  # next day

        if date_to:
            date_to = dateutil_parse(date_to)
        else:
            date_to = date_from + timedelta(days=30)

        rule = rrule(
            freq=DAILY,
            dtstart=date_from,
            until=date_to,
            byweekday=(MO, TU, WE, TH, FR)
        )

        dates = [d.date() for d in list(rule)[:50]]

        availability = defaultdict(list)
        for provider in service.providers.all():
            bookings = Appointment.objects.filter(
                service=service,
                provider=provider,
                starts_at__range=(date_from, date_to),
            )

            taken_dates = set([b.starts_at.date() for b in bookings])
            available_dates = set(dates) - taken_dates

            for d in available_dates:
                availability[d].append(provider)

        availability = [
            {
                'date': d,
                'providers': [ProviderSerializer(p).data for p in providers]
            } for d, providers in availability.items()
        ]

        availability.sort(key=lambda x: x['date'])

        return response.Response(data=availability)

    @decorators.detail_route(methods=['GET'])
    def availability(self, request, pk):
        service = get_object_or_404(Service.objects.filter(pk=pk))
        provider = get_object_or_404(
            Provider.objects.filter(pk=int(self.request.query_params['provider']))
        )

        week_offset = int(self.request.query_params.get('week', '0'))

        date_from = datetime.now() + relativedelta(
            weekday=SU(-1),
            weeks=week_offset,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        date_to = date_from + timedelta(days=7)

        rule = rrule(
            freq=HOURLY,
            dtstart=date_from,
            until=date_to,
            byhour=range(9,18)
        )

        bookings = Appointment.objects.filter(
            service=service,
            provider=provider,
            starts_at__range=(date_from, date_to),
        )

        taken_hours = set()
        for b in bookings:
            taken_hours = taken_hours.union(
                set(list(rrule(HOURLY, b.starts_at.replace(tzinfo=None), until=b.ends_at.replace(tzinfo=None))))
            )

        availability = defaultdict(list)
        for d in rule:
            availability[d.date()].append(d not in taken_hours)

        availability = [
            {
                'date': d,
                'day_of_week': ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'][d.weekday()],
                'available': hour_avail
            } for d, hour_avail in availability.items()
        ]

        availability.sort(key=lambda x: x['date'])

        return response.Response(data=availability)


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


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Appointment
        fields = ('provider', 'service', 'starts_at', 'ends_at')


class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Appointment
        fields = ('provider', 'service', 'starts_at')


class AppointmentViewSet(viewsets.ModelViewSet):
    class Meta(object):
        model = Appointment

    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateAppointmentSerializer

        return AppointmentSerializer

    def perform_create(self, serializer):
        # service = Service.objects.get(pk=serializer.data['service'])
        service = serializer.validated_data['service']
        serializer.save(
            ends_at=(
                serializer.validated_data['starts_at'] + timedelta(seconds=service.duration)
            )
        )
