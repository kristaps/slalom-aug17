from django.db import models


class ServiceCategory(models.Model):
    class Meta(object):
        verbose_name_plural = 'Service categories'

    name = models.CharField(max_length=200)

    def __str__(self):
        return 'Category: {}'.format(self.name)


class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, related_name='services')

    def __str__(self):
        return 'Service: {}'.format(self.name)


class Provider(models.Model):
    name = models.CharField(max_length=200)
    services = models.ManyToManyField(Service, related_name='providers')

    def __str__(self):
        return 'Provider: {}'.format(self.name)
