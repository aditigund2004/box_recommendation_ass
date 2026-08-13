from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """A sellable item with the physical dimensions used for packing."""

    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)

    length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def volume_cm3(self):
        return self.length_cm * self.width_cm * self.height_cm

    @property
    def dimensions(self):
        """Dimensions as a plain tuple, convenient for the packing algorithm."""
        return (float(self.length_cm), float(self.width_cm), float(self.height_cm))


class Box(models.Model):
    """A shippable box type the warehouse can choose from."""

    name = models.CharField(max_length=100, unique=True)

    internal_length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    internal_width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    internal_height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    max_weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["cost"]

    def __str__(self):
        return self.name

    @property
    def volume_cm3(self):
        return self.internal_length_cm * self.internal_width_cm * self.internal_height_cm

    @property
    def dimensions(self):
        return (float(self.internal_length_cm), float(self.internal_width_cm), float(self.internal_height_cm))


class Order(models.Model):
    order_number = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number

    @property
    def total_weight_kg(self):
        return sum((item.quantity * item.product.weight_kg for item in self.items.all()), start=0)

    @property
    def total_volume_cm3(self):
        return sum((item.quantity * item.product.volume_cm3 for item in self.items.all()), start=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.sku}"
