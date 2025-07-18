from openai import OpenAI
from .base import BaseAgent
from .registry import register_agent
from transactions.models import transactions

# import os
# import django
# from transactions.models import transactions
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  
# django.setup()

# def analyst(income, expense, balance, transactions) -> str:
#     transactions_qs = transactions.objects.values('transaction', 'description')
#     formatted_transactions = "\n".join(
#         f"{item['description']} - {item['transaction']}" for item in transactions_qs
#     )
#     client = OpenAI(base_url="https://api.gapgpt.app/v1", api_key='sk-NoXiKQ9JB8qPlauOmNdNqUiS7tLC4Yp6qWLgkp9BGuL0f2Z7')        
#     print(formatted_transactions)
#     prompt = f"""شما نقش یک تحلیل‌گر مالی هوشمند را دارید که باید الگوی خرج‌کرد ماهانه یک کاربر را بر اساس تراکنش‌های واقعی او را خیلی جامع تحلیل کنید.

#     ورودی:
#     - لیستی از تراکنش‌های ماه جاری به زبان فارسی، که هر کدام شامل "توضیح"، "مبلغ"، "تاریخ"، "شماره حساب" و "مانده" است:
#     {formatted_transactions}

#     - جمع کل درآمد (`{income}`) به ریال
#     - جمع کل هزینه (`{expense}`) به ریال
#     - مانده حساب در پایان ماه (`{balance}`)

#     ساختار هر تراکنش:
#     "توضیح: [شرح تراکنش] مبلغ: [عدد با علامت منفی یا مثبت یا شاید هیچ کدوم] مانده: [موجودی حساب] تاریخ: [تاریخ شمسی/شماره‌ای]"
#     مثال تراکنش:
#     "خريد اينترنت:‎-380,000‎ مانده:451,230 تاریخ:0421-19:58"

#     دستورالعمل شما:
#     1. بر اساس توضیحات تراکنش‌ها، دسته‌بندی انجام دهید
#     2. محاسبه کنید هر دسته چند درصد از کل هزینه را تشکیل داده است.
#     3. بررسی کنید بیشترین خرج کاربر در کدام دسته بوده است.
#     4. اگر خرج از درآمد بیشتر بوده، هشدار دهید و راهکار ارائه کنید.
#     5. اگر موجودی کم است، راه‌های بهینه‌سازی خرج را پیشنهاد کنید.
#     6. بر اساس تراکنش‌ها، حداقل مبلغ پس‌انداز پیشنهادی در ماه را تخمین بزنید.
#     7. لحن پاسخ باید دوستانه، روان و فارسی باشد.
#     (میتونی به مانده حساب در تراکنش ها دقت نکنی چون ممکن است اشتباه باشد یا کاربر از چندین کارت بانکی استفاده کند)

#     8. خروجی را در قالب آرایه‌ای از پیشنهادات با ساختار زیر ارائه دهید:

#     ```json
#     [
#     {{
#         "title": "بیشترین هزینه ماه",
#         "message": "بیشترین هزینه شما مربوط به دسته «خرید اینترنت» با مبلغ ۳۸۰٬۰۰۰ ریال بوده است."
#     }},
#     {{
#         "title": "تحلیل نسبت درآمد به هزینه",
#         "message": "درآمد شما بیشتر از هزینه‌ها بوده است و این نشانه خوبی برای مدیریت مالی شماست."
#     }},
#     {{
#         "title": "فرصت پس‌انداز",
#         "message": "با توجه به تراز شما، می‌توانید ماهیانه حداقل ۵۰۰٬۰۰۰ ریال پس‌انداز داشته باشید."
#     }},
#     {{
#         "title": "پیشنهاد مدیریت هزینه‌ها",
#         "message": "سعی کنید هزینه‌های مربوط به «تفریح و خرید آنلاین» را تا حد ۱۵٪ کاهش دهید تا تعادل بهتری برقرار شود."
#     }}
#     ]"""
         
#     response = client.chat.completions.create(
#             model='gpt-4o',
#             messages=[{"role": "user", "content": prompt}]
#         )
#     return response.choices[0].message.content

# print(analyst(18002500000, 2587000, 17999913000, transactions))


@register_agent("analyst")
class Analyzer(BaseAgent):
    def __init__(self, agent_name, model="gpt-4o", endpoint="https://api.gapgpt.app/v1", api_key='sk-NoXiKQ9JB8qPlauOmNdNqUiS7tLC4Yp6qWLgkp9BGuL0f2Z7'):
        super().__init__(agent_name, model, endpoint, api_key)
        self.client = OpenAI(base_url=self.endpoint, api_key=self.api_key)
        
    def analyst(self, income, expense, balance) -> str:
        transactions = transactions.objects.values('transaction', 'description')
        formatted_transactions = "\n".join([
            f"{t['description']}: {t['transaction']}" for t in transactions
        ])        
        print(formatted_transactions)
        prompt = f""" شما نقش یک تحلیل‌گر مالی هوشمند را دارید که باید الگوی خرج‌کرد ماهانه یک کاربر را بر اساس تراکنش‌های واقعی او تحلیل کنید.
                            ورودی:
                            - لیستی از تراکنش‌های ماه جاری به زبان فارسی، که هر کدام شامل "توضیح"، "مبلغ"، "تاریخ"، "شماره حساب" و "مانده" است.
                            {formatted_transactions}
                            
                            - جمع کل درآمد (`{income}`) به ریال
                            - جمع کل هزینه (`{expense}`) به ریال
                            - مانده حساب در پایان ماه (`{balance}`)
                            
                        
                            ساختار هر تراکنش:
                            "توضیح: [شرح تراکنش] مبلغ: [عدد با علامت منفی یا مثبت یا شاید هیچ کدوم] مانده: [موجودی حساب] تاریخ: [تاریخ شمسی/شماره‌ای]"
                            مثال تراکنش:
                            "خريد اينترنت:‎-380,000‎ مانده:451,230 تاریخ:0421-19:58"
                            دستورالعمل شما:
                            1. بر اساس توضیحات تراکنش‌ها، دسته‌بندی انجام دهید (مثلاً: "خرید"، "حمل‌ونقل"، "تفریح"، "قبض"، "درآمد").
                            2. محاسبه کنید هر دسته چند درصد از کل هزینه را تشکیل داده است.
                            3. بررسی کنید بیشترین خرج کاربر در کدام دسته بوده است.
                            4. اگر خرج از درآمد بیشتر بوده، هشدار دهید و راهکار ارائه کنید.
                            5. اگر موجودی کم است، راه‌های بهینه‌سازی خرج را پیشنهاد کنید.
                            6. بر اساس تراکنش‌ها، حداقل مبلغ پس‌انداز پیشنهادی در ماه را تخمین بزنید.
                            7. لحن پاسخ باید دوستانه، روان و فارسی باشد.
                            (.میتونی به مانده حساب در تراکنش ها دقت نکنی چون ممکن است اشباه باشد یا کاربر از چندین کارت بانکی استفاده کند)
                            8. خروجی را در قالب آرایه‌ای از پیشنهادات با ساختار زیر ارائه دهید:

                            ```json
                            [
                            {
                                "title": "بیشترین هزینه ماه",
                                "message": "بیشترین هزینه شما مربوط به دسته «خرید اینترنت» با مبلغ ۳۸۰٬۰۰۰ ریال بوده است."
                            },
                            {
                                "title": "تحلیل نسبت درآمد به هزینه",
                                "message": "درآمد شما بیشتر از هزینه‌ها بوده است و این نشانه خوبی برای مدیریت مالی شماست."
                            },
                            {
                                "title": "فرصت پس‌انداز",
                                "message": "با توجه به تراز شما، می‌توانید ماهیانه حداقل ۵۰۰٬۰۰۰ ریال پس‌انداز داشته باشید."
                            },
                            {
                                "title": "پیشنهاد مدیریت هزینه‌ها",
                                "message": "سعی کنید هزینه‌های مربوط به «تفریح و خرید آنلاین» را تا حد ۱۵٪ کاهش دهید تا تعادل بهتری برقرار شود."
                            }
                            ]
                    """
        response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
        return response.choices[0].message.content