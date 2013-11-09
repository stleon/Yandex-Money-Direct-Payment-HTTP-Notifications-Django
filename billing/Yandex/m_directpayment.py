from django.db import models
from datetime import *

from billing.operations import Credit

# Required for hash computing and evaluation
import hashlib

# Secret from Yandex Money account https://sp-money.yandex.ru/myservices/online.xml
NOTIFICATION_SECRET = '000000000000000000000000'

from commons.handler import Handle

class TransactionsYandexDirectPaymentManager(models.Manager):
	def Log(self, request):
		result = None
		
		# Agreement on abbreviations and variables to be used in elements
		NOTIFICATION_TYPE	= 'notification_type'
		OPERATION_ID		= 'operation_id'
		AMOUNT				= 'amount'
		CURRENCY			= 'currency'
		DATETIME			= 'datetime'
		SENDER				= 'sender'
		CODEPRO				= 'codepro'
		LABEL				= 'label'
		SHA1_HASH_YANDEX	= 'sha1_hash'

		if request.method == "POST":
			transaction = TransactionsYandexDirectPayment()
			transaction_id = None
			purses_object = None
			codepro = "true"
			
			if NOTIFICATION_TYPE in request.POST:
				transaction.notification_type = request.POST[NOTIFICATION_TYPE]
			if OPERATION_ID in request.POST:
				transaction.operation_id = request.POST[OPERATION_ID]
				transaction_id = transaction.operation_id
			if CURRENCY in request.POST:
				transaction.currency = request.POST[CURRENCY]
			if DATETIME in request.POST:
				transaction.date_time = request.POST[DATETIME]
			if SENDER in request.POST:
				transaction.sender = request.POST[SENDER]
			if CODEPRO in request.POST:
				codepro = request.POST[CODEPRO]
				transaction.codepro = codepro
			if LABEL in request.POST:
				transaction.label = request.POST[LABEL]
				purse_hash = transaction.label
				purses_object = Purses.objects.Get(purse_hash = purse_hash)
				if AMOUNT in request.POST and request.POST[AMOUNT]:
					amount = float(request.POST[AMOUNT])
				else:
					amount = 0
			if AMOUNT in request.POST:
				transaction.amount = request.POST[AMOUNT]
			if SHA1_HASH_YANDEX in request.POST:
				transaction.sha1_hash = request.POST[SHA1_HASH_YANDEX]
			
			try:
				transaction.save()
			except Exception as exc:
				message = "TransactionsYandexDirectPayment.Log exception in transaction.save() occured: %s" % exc
				Handle(message)
				return result
			
			# Code for landing money in our system
			# Order and content according to http://api.yandex.ru/money/doc/dg/reference/notification-p2p-incoming.xml
			SHA1_HASH_OURS =	request.POST[NOTIFICATION_TYPE] \
				+ '&' + \
				request.POST[OPERATION_ID] \
				+ '&' + \
				request.POST[AMOUNT] \
				+ '&' + \
				request.POST[CURRENCY] \
				+ '&' + \
				request.POST[DATETIME] \
				+ '&' + \
				request.POST[SENDER] \
				+ '&' + \
				request.POST[CODEPRO] \
				+ '&' + \
				NOTIFICATION_SECRET \
				+ '&' + \
				request.POST[LABEL]
		
			sha1_hash_ours = hashlib.sha1(SHA1_HASH_OURS).hexdigest()
			sha1_hash_yandex = request.POST[SHA1_HASH_YANDEX]
		
			if sha1_hash_ours == sha1_hash_yandex:
				if transaction_id:
					if codepro == "false":
						OBJECT_TYPE = 'purse'
						REASON = 'fund'

						credit_result = Credit()
						if credit_result:
							result = True
						else:
							message = "TransactionsYandexDirectPayment.Log error Credit operation resulted in False for account_id: %s" % account_id
							Handle(message)
					else:
						message = "TransactionsYandexDirectPayment.Log error Transaction has not CUSTOM key so I don't know what's the purse id should be used. Transaction id is: %s" % transaction.txn_id
						Handle(message)
				else:
					message = "TransactionsYandexDirectPayment.Log error Transaction has not OPERATION_ID key so I don't know what's the purse id should be used."
					Handle(message)
			else:
				message = "TransactionsYandexDirectPayment.Log error hash string from sender (we supposed it was Yandex Money) not matched! Looks like a hack"
				Handle(message)
		return result
		
class TransactionsYandexDirectPayment(models.Model):
	notification_type = models.TextField(null = True)
	operation_id = models.TextField(null = True)
	amount = models.FloatField(null = True)
	currency = models.TextField(null = True)
	date_time = models.TextField(null = True)
	sender = models.TextField(null = True)
	codepro = models.TextField(null = True)
	label = models.TextField(null = True)
	sha1_hash = models.TextField(null = True)
	date_lastupdated = models.DateTimeField(null = False, default = datetime.utcnow)
	
	objects = TransactionsYandexDirectPaymentManager()

	def __unicode__(self):
		return self.id

	class Meta:
		db_table = "transactionsyandexdirectpayment"
		ordering = ('id',)
