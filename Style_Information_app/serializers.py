from rest_framework import serializers
from .models import Customer, StyleInfo

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_name']

class StyleInfoSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = StyleInfo
        fields = [
            'id',
            'customer',
            'season',
            'style_no',
            'style_description',
            'program',
            'production_line',
            'order_qty',
            'apm',
            'technician',
            'qc',
            'qa',
            'tqs',
            'comments',
            'created_at'
        ]
