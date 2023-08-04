from rest_framework import serializers
from wallet.models import TransactionCategory

class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['uuid', 'name', 'parent']
