from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random


class randConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		#Add channel_name to the client session
		self.scope["session"]["channel_name"]=self.channel_name
		self.scope["session"].save()
		async_to_sync(self.channel_layer.send)(self.channel_name, {'type': 'status','status':self.scope["session"]["status"]})
	
	def disconnect(self, close_code):
		pass
	
	def status(self, event):
		#Send the number to client for dev purposes only delete that in prod
		self.send(text_data=json.dumps({'status':event['status']}))
