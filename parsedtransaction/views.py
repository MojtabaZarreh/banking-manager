from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import ParsedTransaction
from django.contrib import messages
from agents.registry import get_agent
from agents import analyst_agent
from django.http import JsonResponse
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import re

@login_required
def monthly_summary_view(request):
    month = request.GET.get('month')
    
    if not month or not month.isdigit() or not (1 <= int(month) <= 12):
            return JsonResponse({'error': 'ماه نامعتبر است'}, status=400)

    month_str = f"{int(month):02d}"
    filtered = ParsedTransaction.objects.filter(date_time__regex=rf'^1404/{month_str}/').filter(transaction__user = request.user)
 
    income = filtered.filter(type=1).aggregate(total=Sum('amount'))['total'] or 0
    expense = filtered.filter(type=-1).aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    
    return JsonResponse({
        'month': month_str,
        'income': income,
        'expense': expense,
        'balance': balance
    })
  
@login_required    
def monthly_suggestions_view(request):
    month = request.GET.get('month')
    income = request.GET.get('income')
    expense = request.GET.get('expense')
    balance = request.GET.get('balance')

    if not all([income, expense, balance]):
        return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)

    key_string = f"{income}-{expense}-{balance}-{request.user.id}"
    cache_key = "monthly_suggestions_" + hashlib.md5(key_string.encode()).hexdigest()

    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse({'suggestions': cached_data})

    try:
        agent = get_agent("analyst", agent_name="LLMAnalystAgent")
        suggestions = agent.analyst(request, int(income), int(expense), int(balance), month)

        suggestions = re.sub(r"^```json|```$", "", suggestions.strip()).strip()
        suggestions = json.loads(suggestions)

        cache.set(cache_key, suggestions, timeout=3600)
    except Exception as e:
        return JsonResponse({'error': f'خطا در پردازش تحلیل: {str(e)}'}, status=500)

    return JsonResponse({'suggestions': suggestions})


@csrf_exempt
def ocr_transaction_view(request):
    image = request.FILES.get('image')

    if not image or not isinstance(image, InMemoryUploadedFile):
        return JsonResponse({'error': 'تصویر معتبر ارسال نشده است'}, status=400)

    try:
        agent = get_agent("ocr", agent_name="LLMOCRAgent")

        result = agent.ocr(image)

        if not result:
            return JsonResponse({'error': 'تحلیل تصویر ناموفق بود'}, status=500)

        print(result)
        transaction = ParsedTransaction.objects.create(
            type=result.get('type'),
            amount=result.get('amount'),
            account=result.get('account'),
            balance=result.get('balance'),
            date_time=result.get('date_time')
        )
        
        return JsonResponse({'transaction_id': transaction.id})

    except Exception as e:
        print(result)
        return JsonResponse({'error': f'خطا در ثبت تراکنش: {str(e)}'}, status=500)