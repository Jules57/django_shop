from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    wallet = models.DecimalField(decimal_places=2, max_digits=8, default=10000)
    image = models.ImageField(upload_to='shop/static/shop/images/', max_length=100, null=True)


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='shop/static/shop/images/', max_length=100, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id])


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchased')
    product_quantity = models.PositiveIntegerField()
    bought_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} bought by {self.user} at {self.bought_at}'


class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='returned')
    returned_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.purchase.product.title} returned by {self.purchase.user}'
