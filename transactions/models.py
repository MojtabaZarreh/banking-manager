from django.db import models
from persiantools.jdatetime import JalaliDateTime
from django.contrib.auth.models import User

class transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='transaction/', null=True, blank=True)
    date_time = models.CharField(max_length=20, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.date_time:
            jalali_date = JalaliDateTime.now().strftime('%Y/%m/%d')
            self.date_time = jalali_date
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.description