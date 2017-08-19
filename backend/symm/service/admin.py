from django.contrib import admin


# Register your models here.
from .models import Provider, Service, ServiceCategory


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name')


class ProviderAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name')


class ServiceAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name', 'price_low', 'price_high', 'get_duration')

    def get_duration(self, obj):
        if obj.duration is None:
            return 'Unknown'

        return '{}h'.format(obj.duration / 3600)
    get_duration.verbose_name = 'Duration'



admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Service, ServiceAdmin)
