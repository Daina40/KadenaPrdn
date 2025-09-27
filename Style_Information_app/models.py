from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.customer_name


class StyleInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="styles")
    season = models.CharField(max_length=100, blank=True, null=True)
    style_no = models.CharField(max_length=100, blank=True, null=True)
    style_description = models.TextField(blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    production_line = models.CharField(max_length=100, blank=True, null=True)
    order_qty = models.PositiveIntegerField(blank=True, null=True)
    apm = models.CharField(max_length=100, blank=True, null=True)
    technician = models.CharField(max_length=100, blank=True, null=True)
    qc = models.CharField(max_length=100, blank=True, null=True)
    qa = models.CharField(max_length=100, blank=True, null=True)
    tqs = models.CharField(max_length=100, blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.style_no}"
