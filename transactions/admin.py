from django.contrib import admin
from .models import transactions

class TransactionsAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(user=request.user)

admin.site.register(transactions, TransactionsAdmin)
