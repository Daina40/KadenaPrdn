from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.customer_name


class StyleInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="styles")
    season = models.CharField(max_length=100, blank=True, null=True)
    style_no = models.CharField(max_length=100, blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    production_line = models.CharField(max_length=100, blank=True, null=True)
    order_qty = models.PositiveIntegerField(blank=True, null=True)
    apm = models.CharField(max_length=100, blank=True, null=True)
    technician = models.CharField(max_length=100, blank=True, null=True)
    qc = models.CharField(max_length=100, blank=True, null=True)
    qa = models.CharField(max_length=100, blank=True, null=True)
    tqs = models.CharField(max_length=100, blank=True, null=True)

    source = models.CharField(
        max_length=50,
        choices=[('overview', 'Overview Add'), ('detail', 'Detail Save')],
        default='overview'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.style_no}"

class StyleDescription(models.Model):
    style = models.ForeignKey(StyleInfo, on_delete=models.CASCADE, related_name="descriptions")
    style_description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.style.style_no} - {self.style_description}"
    
class Comment(models.Model):
    style = models.ForeignKey(StyleInfo, on_delete=models.CASCADE, related_name="comments")
    description = models.ForeignKey(StyleDescription, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    responsible_person = models.CharField(max_length=200, blank=True, null=True)
    process = models.CharField(max_length=200, blank=True, null=True)
    comment_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.style.style_no} - {self.process}"

class StyleImage(models.Model):
    style = models.ForeignKey("StyleInfo", on_delete=models.CASCADE, related_name="images")
    description = models.ForeignKey("StyleDescription", on_delete=models.CASCADE, related_name="images")
    image_name = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name
