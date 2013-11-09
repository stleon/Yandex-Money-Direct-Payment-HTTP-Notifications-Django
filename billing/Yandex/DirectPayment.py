from models import TransactionsYandexDirectPayment

# Required to respond with HTTP error codes on invalid Yandex requests
from django.http import HttpResponse

# Required for POST requests processing with CSRF
from django.views.decorators.csrf import csrf_exempt

# Escaping CSRF for Provider request (cause Provider does not have our csrftoken cookie)
@csrf_exempt
def HTTPNotifications(request):
	result = HttpResponse(status=404)
	
	if TransactionsYandexDirectPayment.objects.Log(request):
		result = HttpResponse(status=200)
	
	return result