from django.forms import ModelForm
from .models import (
    Product,
    Provideer,
    Client,
    RemessionNote,
    Bill,
    Employee,
    SaleDetails,
)


class ProvideerForm(ModelForm):
    class Meta:
        model = Provideer
        fields = [
            "name",
            "second_name",
            "phone",
            "product_sold",
            "street",
            "cp",
            "state",
        ]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "lot",
            "description",
            "generic",
            "administration",
            "unit_price",
        ]


class RemessionNoteForm(ModelForm):
    class Meta:
        model = RemessionNote
        fields = [
            "payment_type",
            "hour_delivery",
            "day_delivery",
            "subtotal",
            "amout",
            "provideer",
        ]
