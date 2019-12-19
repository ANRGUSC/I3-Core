from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product
User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
	seller = serializers.StringRelatedField()
	sensor_type = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = ('seller', 'media', 'title', 'sensor_type', 'description', 'price', 'sale_active', 'sale_price', 'id')
	def to_internal_value(self, data):
		data['seller'] = data['seller'].id
		return super(ProductSerializer,self).to_internal_value(data)
	def get_sensor_type(self, obj):
		n = obj.sensor_type
		if n == 1:
			obj.sensor_type = 'sensor'
		elif n == 2:
			obj.sensor_type = 'actuactor'
		else:
			obj.sensor_type = 'both'
		return obj.sensor_type
