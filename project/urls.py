from django.conf.urls import patterns, include, url

# Dajaxice required
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	# your url patterns go here...
	url(r'^billing/yandex/directpayment/httpnotifications/$', 'billing.Yandex.DirectPayment.HTTPNotifications'),
	# your url patterns go here...

	# Dajaxice required
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
# Dajaxice required, but I'm not sure if I need this too
urlpatterns += staticfiles_urlpatterns()
