# 📌 About Banking Manager
Banking Manager is more than just a simple SMS or receipt reader. It is designed to help users manage their personal finances by analyzing monthly income and expenses extracted from bank transaction slips and SMS messages. Using advanced AI-powered data extraction and analysis techniques, it categorizes your expenditures, identifies which areas consume most of your money, and provides actionable insights and recommendations for better cost management.

Key Functionalities:
Extracts transaction data (amount, date, type, balance) automatically from scanned slips or SMS
Analyzes monthly income vs. expenses and current balance
Highlights categories with highest spending (e.g., groceries, utilities, entertainment)
Provides personalized cost management tips and budgeting suggestions
Helps users gain a clear overview of their financial health over time
This makes Banking Manager a powerful tool for anyone wanting to improve financial discipline and make smarter spending decisions.

# 🧠 Architecture and AI Models
Banking Manager employs a modular agent-based design with two specialized AI agents, each powered by advanced open-source large language models (LLMs) from OpenAI's GPT-OSS series:
OCR Agent: Uses the openai/gpt-oss-20b model to process scanned bank transaction slips. This agent extracts critical transaction data such as amount, account number, date, balance, and transaction type (withdrawal or deposit) with high accuracy.
Analysis Agent: Powered by the larger openai/gpt-oss-120b model, this agent performs deep analysis of the extracted transaction data. It evaluates monthly income and expenses, identifies major spending categories, and generates personalized recommendations to help users optimize their financial management.
This separation of concerns enables Banking Manager to be both scalable and efficient, leveraging the strengths of each model for its respective task. Using cutting-edge open-source GPT-OSS models ensures transparency, flexibility, and state-of-the-art performance without reliance on proprietary closed-source models.

https://github.com/user-attachments/assets/4f647ae2-bd7f-4095-ac5f-867d9694b54f

