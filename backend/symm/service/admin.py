from django.contrib import admin


# Register your models here.
from .models import Provider, Service, ServiceCategory


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name')


class ProviderAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name')


class ServiceAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name')


admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Service, ServiceAdmin)
