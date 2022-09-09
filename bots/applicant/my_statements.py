from app.models import Statement
from app.services import (
    statementservice, 
    supplyservice,
    stringservice
    )
from . import *
from bots import *
from bots.applicant.directive import to_the_typing_product_name
from datetime import datetime

@is_start
def click_statement(update, context):
    update = update.callback_query
    data = str(update.data)

    if 'supplied_statement-' in data:
        *args, id = data.split('-')
        st = statementservice.get_object_by_id(int(id))
        st.status = 'supp'
        st.save()
        bot_answer_callback_query(update, context, get_word('success', update))
        bot_delete_message(update, context)