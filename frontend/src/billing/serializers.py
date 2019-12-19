from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction
User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):
	seller = serializers.StringRelatedField()
	buyer = serializers.StringRelatedField()
	product = serializers.StringRelatedField()
	class Meta:
		model = Transaction
		fields = ('buyer', 'seller', 'product', 'price', 'quantity', 'timestamp')