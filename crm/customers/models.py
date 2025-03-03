from django.db import models


class Customers(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    firstname = models.CharField('Имя клиента', max_length=255)
    lastname = models.CharField('Фамилия клиента', max_length=255, blank=True, null=True)
    language = models.CharField('Язык клиента', max_length=3)
    phone = models.CharField('Телефон клиента', max_length=20)
    address = models.CharField('Адрес клиента', max_length=255, blank=True, null=True)
    car = models.CharField('Машина клиента', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.firstname

    def get_absolute_url(self):
        return f'/customers/{self.id}'

    class Meta:
        verbose_name = 'Customers'
        verbose_name_plural = 'Customers'