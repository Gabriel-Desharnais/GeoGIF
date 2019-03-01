from .models import errorLog
from django.utils import timezone

def logMiddleware(get_response):
    def middleware(request):
        theRequest = request.build_absolute_uri()
        time = timezone.now()
        e = errorLog(request = theRequest, error = "", time = time)
        e.save()
        return get_response(request)
    return middleware
