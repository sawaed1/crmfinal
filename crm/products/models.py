from django.db import models


class Products(models.Model):
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    title = models.CharField('Название товара', max_length=250)
    cost_price = models.DecimalField("Себестоимость", max_digits=10, decimal_places=2)
    retail_price = models.DecimalField("Розничная цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/products/{self.id}'

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'