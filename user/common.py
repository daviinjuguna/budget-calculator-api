
import json
import os
from pathlib import Path

from .models import Expense, Income


def initExpense(user):
    BASE_DIR = Path(__file__).resolve().parent.parent
    income_data = open(os.path.join(BASE_DIR, "income.json"))
    income_json = json.loads(income_data.read())
    expense_data = open(os.path.join(BASE_DIR, "expense.json"))
    expense_json = json.loads(expense_data.read())

    income = Income(
        user=user, income=income_json['income'], amount=income_json['amount'])
    income.save()

    for expense in expense_json:
        expense_ = Expense(
            user=user, expense=expense['name'], recommended=expense['recommended'])
        expense_.save()

    print("ADDEEEDD")
