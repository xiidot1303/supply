from app.models import Statement
from app.services import statementservice
from datetime import datetime

def cancel_overdue_statements():
    now = datetime.now()
    query = statementservice.filter_notconfirmed_statements()
    for obj in query:
        time_delta = now - obj.date
        if time_delta.days > 0:
            statementservice.cancel_statement(obj=obj)