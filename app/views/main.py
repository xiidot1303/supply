from django.http import FileResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_photos(request, file):
    f = open('files/photos/{}'.format(file), 'rb')
    return FileResponse(f)