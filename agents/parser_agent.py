from openai import OpenAI
from .base import BaseAgent
from .registry import register_agent

@register_agent("parser")
class TransactionParser(BaseAgent):
    def __init__(self, agent_name, model="gpt-4o", endpoint="https://api.gapgpt.app/v1", api_key='sk-NoXiKQ9JB8qPlauOmNdNqUiS7tLC4Yp6qWLgkp9BGuL0f2Z7'):
        super().__init__(agent_name, model, endpoint, api_key)
        self.client = OpenAI(base_url=self.endpoint, api_key=self.api_key)

    def parse(self, text: str) -> str:
        prompt = f"""
                    شما یک سیستم استخراج اطلاعات از پیامک‌های بانکی هستید. لطفاً پیامک زیر را بررسی کن و اطلاعات اصلی آن را به‌صورت دقیق در قالب JSON استخراج کن.

                    📩 **پیامک:**
                    {text}

                    📌 **قوانین پردازش:**

                    ۱. فقط خروجی استاندارد JSON بده. بدون هیچ متن توضیحی قبل یا بعد از آن.

                    ۲. کلیدهای مورد انتظار در خروجی فقط این‌ها هستند:
                    - `amount` (عدد خالص، فقط رقم، بدون علامت + یا , یا تومان)
                    - `account` (شماره حساب)
                    - `balance` (موجودی نهایی حساب، فقط عدد خالص)
                    - `datetime` (تاریخ و ساعت تراکنش، به فرمت نوشته‌شده در پیام)
                    - `type` (عددی باشد: واریز = 1، برداشت = -1)

                    ۳. اگر در متن، نوع تراکنش واریز بود (مثلاً "واریز"، "دریافت"، "وصول") مقدار `type` را برابر با **1** قرار بده.
                    اگر برداشت بود (مثلاً "برداشت"، "خرید"، "پرداخت"، "کسر"، "برداشت نقدی") مقدار `type` را **-1** قرار بده.

                    ۴. مقدار `amount` و `balance` باید فقط عدد باشند (مثل: 1250000). همه‌ی علائم فارسی، علامت منفی، تومان، و کاما (,) باید حذف شوند.

                    ۵. اگر مقدار یا فیلدی در متن نبود یا قابل استخراج نبود، مقدار آن را برابر با `null` قرار بده.

                    ۶. همیشه خروجی را فقط با فرمت JSON برگردان. هرگونه متن اضافی ممنوع است.

                    🔁 **نمونه خروجی صحیح:**
                    ```json
                    {{
                    "amount": 380000,
                    "account": "710121355964",
                    "balance": 451230,
                    "datetime": "0421-19:58",
                    "type": -1
                }} """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
