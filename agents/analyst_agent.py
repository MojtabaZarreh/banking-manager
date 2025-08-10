from openai import OpenAI
from .base import BaseAgent
from .registry import register_agent
from transactions.models import transactions
from groq import Groq
from core.config import settings

@register_agent("analyst")
class Analyzer(BaseAgent):
    def __init__(self, agent_name, model="openai/gpt-oss-120b", api_key=settings.Agent2['API_KEY']):
        super().__init__(agent_name, model, api_key)
        #OpenAI
        self.client = Groq(#base_url=self.endpoint, 
                           api_key=self.api_key)
        
    def parse(self, text: str) -> str:
        return "Parse not implemented in this agent."
        
    def analyst(self, request, income, expense, balance, month) -> str:
        transactions_qs = transactions.objects.filter(user=request.user, date_time__regex=rf'^1404/{month}/').values('transaction', 'description')
        formatted_transactions = "\n".join(
            f"{item['description']} - {item['transaction']}" for item in transactions_qs
        )
        prompt = f"""شما نقش یک تحلیل‌گر مالی هوشمند را دارید که باید الگوی خرج‌کرد ماهانه یک کاربر را بر اساس تراکنش‌های واقعی او را خیلی جامع تحلیل کنید.

            ورودی:
            - لیستی از تراکنش‌های ماه جاری به زبان فارسی، که هر کدام شامل "توضیح"، "مبلغ"، "تاریخ"، "شماره حساب" و "مانده" است:
            {formatted_transactions}

            - جمع کل درآمد (`{income}`) به ریال
            - جمع کل هزینه (`{expense}`) به ریال
            - مانده حساب در پایان ماه (`{balance}`)

            ساختار هر تراکنش:
            "توضیح: [شرح تراکنش] مبلغ: [عدد با علامت منفی یا مثبت یا شاید هیچ کدوم] مانده: [موجودی حساب] تاریخ: [تاریخ شمسی/شماره‌ای]"
            مثال تراکنش:
            "خريد اينترنت:‎-380,000‎ مانده:451,230 تاریخ:0421-19:58"

            دستورالعمل شما:
            1. بر اساس توضیحات تراکنش‌ها، دسته‌بندی انجام دهید
            2. محاسبه کنید هر دسته چند درصد از کل هزینه را تشکیل داده است.
            3. بررسی کنید بیشترین خرج کاربر در کدام دسته بوده است.
            4. اگر خرج از درآمد بیشتر بوده، هشدار دهید و راهکار ارائه کنید.
            5. اگر موجودی کم است، راه‌های بهینه‌سازی خرج را پیشنهاد کنید.
            6. بر اساس تراکنش‌ها، حداقل مبلغ پس‌انداز پیشنهادی در ماه را تخمین بزنید.
            7. لحن پاسخ باید دوستانه، روان و فارسی باشد.
            (میتونی به مانده حساب در تراکنش ها دقت نکنی چون ممکن است اشتباه باشد یا کاربر از چندین کارت بانکی استفاده کند)

            8. خروجی را در قالب آرایه‌ای از پیشنهادات با ساختار زیر ارائه دهید:

            ```json
            [
            {{
                "title": "بیشترین هزینه ماه",
                "message": "بیشترین هزینه شما مربوط به دسته «خرید اینترنت» با مبلغ ۳۸۰٬۰۰۰ ریال بوده است."
            }},
            {{
                "title": "تحلیل نسبت درآمد به هزینه",
                "message": "درآمد شما بیشتر از هزینه‌ها بوده است و این نشانه خوبی برای مدیریت مالی شماست."
            }},
            {{
                "title": "فرصت پس‌انداز",
                "message": "با توجه به تراز شما، می‌توانید ماهیانه حداقل ۵۰۰٬۰۰۰ ریال پس‌انداز داشته باشید."
            }},
            {{
                "title": "پیشنهاد مدیریت هزینه‌ها",
                "message": "سعی کنید هزینه‌های مربوط به «تفریح و خرید آنلاین» را تا حد ۱۵٪ کاهش دهید تا تعادل بهتری برقرار شود."
            }}
            
            ساختار مثل بالا باشد اما توضیحات یا message ها طولانی تر و دقیق تر باشد و نکات مهم رو توضیح دهد
            ]"""
        
        response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
        return response.choices[0].message.content