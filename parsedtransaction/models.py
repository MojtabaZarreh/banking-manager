from django.db import models
from persiantools.jdatetime import JalaliDateTime
from transactions.models import transactions


class ParsedTransaction(models.Model):
    
    TRANSACTION_TYPE_CHOICES = (
        (1, 'Deposit'),    
        (-1, 'Withdrawal') 
    )
        
    transaction = models.ForeignKey(transactions, on_delete=models.CASCADE, related_name='parsed')
    amount = models.BigIntegerField(null=False)
    account = models.CharField(max_length=20, null=True, blank=True)
    balance = models.BigIntegerField(null=True, blank=True)
    date_time = models.CharField(max_length=20)
    type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.date_time:
            jalali_date = JalaliDateTime.now().strftime('%Y/%m/%d - %H:%M:%S')
            self.date_time = jalali_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction} | {self.amount} | {self.date_time} | {self.transaction.user}"
