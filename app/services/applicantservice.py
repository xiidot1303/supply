from app.models import Applicant

def get_or_create(user_id):
    obj = Applicant.objects.get_or_create(user_id=user_id)
    

def get_object_by_user_id(user_id):
    obj = Applicant.objects.get(user_id=user_id)
    return obj

def get_object_by_update(update):
    obj = Applicant.objects.get(user_id=update.message.chat.id)
    return obj