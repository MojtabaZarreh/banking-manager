from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import ParsedTransaction
import re

def monthly_summary_view(request):
    month = request.GET.get('month')
    
    if not month or not month.isdigit() or not (1 <= int(month) <= 12):
            return JsonResponse({'error': 'ماه نامعتبر است'}, status=400)

    month_str = f"{int(month):02d}"
    filtered = ParsedTransaction.objects.filter(date_time__regex=rf'^1404/{month_str}/')

    income = filtered.filter(type=1).aggregate(total=Sum('amount'))['total'] or 0
    expense = filtered.filter(type=-1).aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    
    return JsonResponse({
        'month': int(month),
        'income': income,
        'expense': expense,
        'balance': balance
    })