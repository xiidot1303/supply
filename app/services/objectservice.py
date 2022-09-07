from app.models import Object




def is_msg_object_title(msg):
    if Object.objects.filter(title__icontains=msg):
        return True
    return False

def get_object_by_msg(msg):
    obj = Object.objects.filter(title__icontains=msg)[0]
    return obj