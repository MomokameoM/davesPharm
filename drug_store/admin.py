from django.contrib import admin
from .models import (
    Product,
    Provideer,
    Client,
    RemessionNote,
    Bill,
    Employee,
    SaleDetails,
)


admin.site.register(Product)
admin.site.register(Provideer)
admin.site.register(Client)
admin.site.register(RemessionNote)
admin.site.register(Bill)
admin.site.register(Employee)
admin.site.register(SaleDetails)
