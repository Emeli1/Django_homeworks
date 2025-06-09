from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=50)
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.id}:'\
               f'{self.name},'\
               f'{self.image},' \
               f'{self.price},' \
               f'{self.release_date},'\
               f'{self.lte_exists},'\
               f'{self.slug}'



