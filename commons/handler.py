from django.conf import settings

# This function Handle could be used to:
# 	write log (demonstrated below), 
#	send email notification, 
#	send sms notification,
#	etc.
# in case of special instructions from **kwargs. So, you just call Handle(message)

def Handle(*args, **kwargs):
	result = None

	if args:
		message = args[0]
	elif kwargs:
		MESSAGE = 'message'
		message = kwargs[MESSAGE]
	else:
		message = "An error occured and commons.handler.Handle has been called, \
		but no message had been provided for Handle..."
				
	if settings.DEBUG:
		print message
		result = True
	else:
		pass # do not write Handler's log in case of production
		
	return result