
import json
import os
from pathlib import Path

from .models import Expense


def initExpense(user):
    BASE_DIR = Path(__file__).resolve().parent.parent
    expense_data = open(os.path.join(BASE_DIR, "expense.json"))
    expense_json = json.loads(expense_data.read())

    for expense in expense_json:
        expense_ = Expense(
            user=user, expense=expense['name'], recommended=expense['recommended'])
        expense_.save()

    print("ADDEEEDD")
