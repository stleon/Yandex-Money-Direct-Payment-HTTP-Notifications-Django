from billing.models import Purses
from billing.operations import Credit

# Required for matching only valid-formatted requests from Yandex
import re

# Required to respond with HTTP error codes on invalid Yandex requests
from django.http import HttpResponse

# Required for hash computing and evaluation
import hashlib

# Required for POST requests processing with CSRF
from django.views.decorators.csrf import csrf_exempt

# Secret from Yandex Money account https://sp-money.yandex.ru/myservices/online.xml
NOTIFICATION_SECRET = 'CbJgZDJ13J7onxBlgDRaRjUE'

# Escaping CSRF for Yandex Money request (cause YM does not have our csrftoken cookie)
@csrf_exempt
def HTTPNotifications(request):
	result = HttpResponse(status=404)
	
	# Agreement on abbreviations and variables to be used in elements
	NOTIFICATION_TYPE	= 'notification_type'
	OPERATION_ID		= 'operation_id'
	AMOUNT				= 'amount'
	CURRENCY			= 'currency'
	DATETIME			= 'datetime'
	SENDER				= 'sender'
	CODEPRO				= 'codepro'
	LABEL				= 'label'
	SHA1_HASH			= 'sha1_hash'
	
	# Agreement on regexp format for each element
	if request.method == "POST":
		request_expected_elements = {
			NOTIFICATION_TYPE:	'^(p2p-incoming)$',			#p2p-incoming
			OPERATION_ID:		'^([0-9]{1,256})$',			#1234567
			AMOUNT:				'^([0-9]{1,6}\.[0-9]{2})$',	#300.00
			CURRENCY:			'^(643)$',					#643
			DATETIME:			'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z])$',	#2011-07-01T09:00:00Z
			SENDER:				'^([0-9A-Z]+)$',			#41001XXXXXXXX
			CODEPRO:			'^(false)$',				#false
			LABEL:				'^([0-9a-z]{1,256})$',		#hjg314kjh24312769z2187t0ehio
			SHA1_HASH:			'^([0-9a-z]+)$',			#090a8e7ebb6982a7ad76f4c0f0fa5665d741aafa
		}
	
		input_correct = {}
		input_errors = {}

		# Filling up input_correct and input_errors dictionaries with regexp
		for element, regexp in request_expected_elements.iteritems():
			try:
				# utf-8 for in-label possible values
				value_received = request.POST[element].encode('utf-8')
				value_valid = re.search(regexp, value_received)
			
				if value_valid:
					input_correct.update({element: value_valid.group()})
				else:
					input_errors.update({element: value_received})
		
			except Exception as exc:
				print "Yandex Money HTTPNotifications exception occured: %s" % exc
				print "Looks like Yandex has broken an expected element: %s" % element
				print "Value received: %s" % value_received
				print "Value format expected: %s" % regexp
				return result
				
		# Uncomment for debugging input_values
		print "input_correct dictionary: ", input_correct
		print "input_errors dictionary: ", input_errors
	
		if input_errors:
			print "We have not empty dictionary of errors. I do not process this transaction further"
			return result

		# Order and content according to http://api.yandex.ru/money/doc/dg/reference/notification-p2p-incoming.xml
		sha1_hash_string =	input_correct[NOTIFICATION_TYPE] \
							+ '&' + \
							input_correct[OPERATION_ID] \
							+ '&' + \
							input_correct[AMOUNT] \
							+ '&' + \
							input_correct[CURRENCY] \
							+ '&' + \
							input_correct[DATETIME] \
							+ '&' + \
							input_correct[SENDER] \
							+ '&' + \
							input_correct[CODEPRO] \
							+ '&' + \
							NOTIFICATION_SECRET \
							+ '&' + \
							input_correct[LABEL]

		sha1_hash_ours = hashlib.sha1(sha1_hash_string).hexdigest()
		sha1_hash_yandex = input_correct[SHA1_HASH]

		if not sha1_hash_ours == sha1_hash_yandex:
			print "Hash string from Yandex Money not matched! Someone tries to break us"
			return result

		# Your code for landing money in your system
		if AMOUNT in input_correct and LABEL in input_correct:
			amount = input_correct[AMOUNT]
			purse_hash = input_correct[LABEL]
			
			purses_object = Purses.objects.Get(purse_hash = purse_hash)
			if purses_object:
				account_id = purses_object.account_id
				
				credit_result = Credit(account_id = account_id, amount = amount, object_type = 'purse', object_id = purses_object.id)
				if credit_result:
					result = HttpResponse(status=200)

	return result
