from app.models import Applicant
from app.services import stringservice
from bots import *

def get_or_create(user_id):
    obj = Applicant.objects.get_or_create(user_id=user_id)
    

def get_object_by_user_id(user_id):
    obj = Applicant.objects.get(user_id=user_id)
    return obj

def get_object_by_update(update):
    obj = Applicant.objects.get(user_id=update.message.chat.id)
    return obj

def notify_user_about_statement_status(statement, supply=None):
    user = statement.user
    text = stringservice.statement_status_for_applicant(statement, supply)
    send_newsletter(applicant_bot, user.user_id, text)