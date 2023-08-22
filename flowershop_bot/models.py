from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')
    height = models.DecimalField(max_digits=5, decimal_places=0)
    width = models.DecimalField(max_digits=5, decimal_places=0)
    composition = models.ManyToManyField(Item, through='Composition')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Composition(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        related_name='compositions',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name


class Quiz(models.Model):
    OCCASIONS = [
        ('wedding', 'Свадьба'),
        ('birthday', 'День рождения'),
        ('no_occasion', 'Без повода')
    ]
    PRICE_RANGES = [
        ('under-1000', 'До 1 000 руб'),
        ('1000-5000', '1 000 - 5 000 руб'),
        ('over-5000', 'от 5 000 руб'),
        ('no-matter', 'Не имеет значения')
    ]

    occasion = models.CharField(max_length=20, choices=OCCASIONS)
    price_range = models.CharField(max_length=20, choices=PRICE_RANGES)
    bouquets = models.ManyToManyField(Bouquet, related_name='occasions')

    def __str__(self):
        return f"{self.get_occasion_display()} - {self.get_price_range_display()}"
