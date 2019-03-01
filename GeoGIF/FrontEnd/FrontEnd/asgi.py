#import os
#import channels.asgi

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chanelSimpleDemo.settings')
#channel_layer = channels.asgi.get_channel_layer()
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FrontEnd.settings")
django.setup()
application = get_default_application()
