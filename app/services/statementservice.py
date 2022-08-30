from app.models import Statement
from app.services import applicantservice, apiservice

def create_and_get_object_by_update(update):
    user = applicantservice.get_object_by_user_id(update.message.chat.id)
    obj = Statement.objects.create(user=user)
    return get_object_by_id(obj.pk)

def get_object_by_id(id):
    return Statement.objects.get(pk=id)

def get_current_object_by_update(update):
    obj = Statement.objects.get(status=None, user__user_id=update.message.chat.id)
    return obj

def filter_current_objects_by_update(update):
    user = applicantservice.get_object_by_update(update)
    objects = Statement.objects.filter(status=None, user=user)
    return objects

def cancel_statement_by_id(pk):
    obj = get_object_by_id(pk)
    obj.status = 'cancel'
    obj.save()
    apiservice.cancel_statement_api(obj)