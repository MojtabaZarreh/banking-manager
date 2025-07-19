from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import ParsedTransaction
from django.contrib import messages
from agents.registry import get_agent
from agents import analyst_agent
from django.http import JsonResponse
from django.core.cache import cache
import hashlib
import json
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
    
def monthly_suggestions_view(request):
    income = request.GET.get('income')
    expense = request.GET.get('expense')
    balance = request.GET.get('balance')

    if not all([income, expense, balance]):
        return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)

    key_string = f"{income}-{expense}-{balance}"
    cache_key = "monthly_suggestions_" + hashlib.md5(key_string.encode()).hexdigest()

    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse({'suggestions': cached_data})

    try:
        agent = get_agent("analyst", agent_name="LLMAnalystAgent", model="gpt-4o")
        suggestions = agent.analyst(int(income), int(expense), int(balance))

        suggestions = re.sub(r"^```json|```$", "", suggestions.strip()).strip()
        suggestions = json.loads(suggestions)

        cache.set(cache_key, suggestions, timeout=3600)
    except Exception as e:
        return JsonResponse({'error': f'خطا در پردازش تحلیل: {str(e)}'}, status=500)

    return JsonResponse({'suggestions': suggestions})