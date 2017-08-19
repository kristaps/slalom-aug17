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
    price_high = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=0)
    price_low = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=0)
    duration = models.PositiveIntegerField(default=14400, null=True)

    def __str__(self):
        return 'Service: {}'.format(self.name)


class Provider(models.Model):
    name = models.CharField(max_length=200)
    services = models.ManyToManyField(Service, related_name='providers')
    rating = models.PositiveIntegerField(default=5, choices=[(i, str(i)) for i in (1, 2, 3, 4, 5)])

    def __str__(self):
        return 'Provider: {}'.format(self.name)
