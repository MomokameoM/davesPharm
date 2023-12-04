from django.db import models
from django.contrib.auth.models import User


class Provideer(models.Model):
    name = models.CharField(max_length=70, null=False)
    second_name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=10, null=False)
    product_sold = models.CharField(max_length=30, null=False)
    street = models.CharField(max_length=40, null=False)
    cp = models.CharField(max_length=5, null=False)
    state = models.CharField(max_length=40, null=False)

    def __str__(self):
        return f"Proveedor: {self.name} {self.second_name}"


class RemessionNote(models.Model):
    PAYMENT_CHOICES = [
        ("tarjeta", "Tarjeta"),
        ("efectivo", "Efectivo"),
    ]
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="tarjeta",
    )
    hour_order = models.TimeField(auto_now_add=True)
    day_order = models.DateField(auto_now_add=True)
    hour_delivery = models.TimeField(auto_now_add=False, null=False)
    day_delivery = models.DateField(auto_now_add=False, null=False)
    subtotal = models.IntegerField()
    amout = models.IntegerField()
    provideer = models.ForeignKey(Provideer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nota de Remisión - Proveedor: {self.provideer.name} - Tipo de Pago: {self.get_payment_type_display()}"


class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    lot = models.CharField(max_length=10)
    purchase_date = models.DateField(auto_now_add=True, null=False)
    expiration_date = models.DateField(null=False)
    description = models.TextField(max_length=500, null=False)
    generic = models.BooleanField(default=False, null=False)
    administration = models.CharField(max_length=30, null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"Producto: {self.name}"


class Employee(models.Model):
    name = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, null=False)
    three_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=10, null=False)

    def __str__(self):
        return f"Empleado: {self.name} {self.second_name}"


class Client(models.Model):
    name = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, null=False)
    three_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=10, null=False)
    rfc = models.CharField(max_length=13, null=False)

    def __str__(self):
        return f"Cliente: {self.name}"


class SaleDetails(models.Model):
    sale_date = models.DateField(auto_now_add=True)
    sale_hour = models.TimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField(default=1, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"Detalle de Venta - Producto: {self.product.name} - Cantidad: {self.quantity_sold}"


class Bill(models.Model):
    rfc_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products_purchased = models.OneToOneField(SaleDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura - Cliente: {self.rfc_client.name} - Detalles de Venta: {self.products_purchased}"
