from django.contrib import admin
from .models import ParsedTransaction
from transactions.models import transactions

class ParsedTransactionAdmin(admin.ModelAdmin):
    
    # search_fields = ['user__username', 'transaction']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "transaction":
            if not request.user.is_superuser:
                kwargs["queryset"] = transactions.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(transaction__user=request.user)

admin.site.register(ParsedTransaction, ParsedTransactionAdmin)