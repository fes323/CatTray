from rest_framework import generics
from .models import TransactionCategory
from .serializers import TransactionCategorySerializer

class TransactionCategoryListApiView(generics.ListCreateAPIView):
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        user = self.request.user.profile
        return TransactionCategory.objects.filter(user=user)
