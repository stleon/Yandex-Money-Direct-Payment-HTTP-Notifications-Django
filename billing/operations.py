from billing.models import Purses, Billinghistory
from commons.handler import Handle

def Process(**kwargs):
	result = None
	
	purses_object = Purses.objects.Update(**kwargs)
	if purses_object:
		billinghistory_object = Billinghistory.objects.Update(**kwargs)
		if billinghistory_object:
			result = billinghistory_object
		else:
			message = "billing.operations.Process error: \
			billinghistory_object = Billinghistory.objects.Update(**kwargs) \
			returned false - we didn't log transaction to billinghistory, \
			but charged a Purse! Kwargs were: %s" % kwargs
			Handle(message)
	else:
		message = "Operations.Process error: \
		purses_object = Purses.objects.Update(**kwargs) \
		returned false - we didn't update a Purse after some transaction. \
		Kwargs were: %s" % kwargs
		Handle(message)

	return result

def Debet(**kwargs):
	kwargs['operation'] = 'debet'
	return Process(**kwargs)

def Credit(**kwargs):
	kwargs['operation'] = 'credit'
	return Process(**kwargs)

def Refund(**kwargs):
	kwargs['operation'] = 'special'
	return Process(**kwargs)