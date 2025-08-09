from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from master.urls import master
from .models import transactions
from parsedtransaction.models import ParsedTransaction
from django.contrib import messages
from agents.registry import get_agent
from agents import parser_agent
from django.http import JsonResponse
import json
import re

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        user_text = request.POST.get('smsContent')
        description = request.POST.get('description')
        
        if not user_text:
            messages.error(request, "متن پیامک را وارد کنید.")
            return redirect(request.path)
        
        tr = transactions.objects.create(user=request.user, transaction=user_text, description=description)
        
        try:
            agent = get_agent(
                "parser",
                agent_name="LLMParsedTransaction",
            )
             
            raw_result = agent.parse(user_text, description)
            clean_result = re.sub(r"^```json|```$", "", raw_result.strip()).strip()
            result = json.loads(clean_result)
            ParsedTransaction.objects.create(
                transaction=tr,
                amount=result.get('amount'),
                account=result.get('account'),
                balance=result.get('balance'),
                type=result.get('type')
            )
            messages.success(request, f"تراکنش با موفقیت ثبت و تحلیل شد.")
                
        except Exception as e:
            messages.error(request, f"خطا در پردازش تراکنش: {str(e)}")
        
    return redirect('master')
      
def transaction_list_api(request):
    if request.method == 'GET':
        data = []
        for tr in transactions.objects.filter(user=request.user).order_by('-created_at'):
            parsed = tr.parsed.first()  
            tr_type = parsed.type if parsed else None 

            data.append({
                'id': tr.id,
                'smsContent': tr.transaction,
                'description': tr.description,
                'date': tr.date_time,
                'type': tr_type
                
            })
        return JsonResponse(data, safe=False)