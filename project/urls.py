from django.conf.urls import patterns, include, url

# Dajaxice required
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
# Dajaxice required, but I'm not sure if I need this
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Django admin requires
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
	
	url(r'^$', 'views.views.Main'),
	url(r'^/$', 'views.views.Main'),
	
	
	url(r'^services/$', 'views.views.Services'),
	url(r'^prices/$', 'costs.views.Prices'),
	url(r'^prices/(?P<campaign>.*)/(?P<add_group>.*)/$', 'costs.views.Advertisement'),
	url(r'^blog/.*$', 'views.views.Blog'),
	url(r'^about/$', 'views.views.About'),
	url(r'^contacts/$', 'views.views.Contacts'),

	url(r'^capabilities/$', 'views.views.Capabilities'),
	url(r'^advantages/$', 'views.views.Advantages'),
	url(r'^benefits/$', 'views.views.Benefits'),

	url(r'^signup/$', 'signup.views.Signup'),
	url(r'^signupcomplete/$', 'signup.views.SignupComplete'),
	url(r'^verification/email/(?P<email_code>[\w]+)/$', 'signup.views.EmailVerification'),
	url(r'^verification/phone/$', 'signup.views.ContactPhoneVerification'),
	
	url(r'^account/login/$', 'login.views.Login'),
	url(r'^account/logout/$', 'login.views.Logout'),
	url(r'^account/login/forgot/$', 'login.views.Forgot'),
	url(r'^account/login/forgot/completed/$', 'login.views.ForgotOk'),
	url(r'^account/login/forgot/restore/(?P<email_code>[\w]+)/$', 'login.views.EmailVerification'),
	url(r'^account/login/forgot/restore/$', 'login.views.ForgotRestore'),
		
	url(r'^account/telephony/settings/$', 'settings.views.Settings'),
	url(r'^account/telephony/history/$', 'callshistory.views.Callhistory'),

	url(r'^account/administration/settings/$', 'administration.views.Settings'),
	url(r'^account/administration/documents/$', 'administration.views.Documents'),
	url(r'^account/administration/contract/$', 'administration.views.SignContract'),
	url(r'^account/administration/documents/contract/$', 'administration.views.Contract'),
		
	url(r'^account/administration/billing/funds/$', 'billing.views.Funds'),	
	url(r'^account/administration/billing/history/$', 'billing.views.History'),
	url(r'^account/billing/yandex/directpayment/httpnotifications/$', 'billing.paymentgateways.Yandex.DirectPayment.HTTPNotifications'),
	url(r'^account/billing/paypal/expresscheckout/instantpaymentnotifications/$', 'billing.paymentgateways.PayPal.ExpressCheckout.IPN'),
	url(r'^admin/billing/bill/$', 'billing.paymentgateways.Invoice.BillPayment.Receive'),

	url(r'^generate/(?P<document_type>[\w]+)/(?P<document_parameter>[\w.]+)/$', 'rendering.views.Generate'),
	url(r'^render/(?P<document_type>[\w]+)/(?P<document_id>[\w.]+)/$', 'rendering.views.Render'),
	url(r'^display/(?P<document_type>[\w]+)/(?P<document_id>[\w]+)/$', 'rendering.views.Display'),
	url(r'^html2pdf/(?P<document_type>[\w]+)/(?P<document_id>[\w.]+)/$', 'rendering.views.HTML2PDF'),
	
	url(r'^emails/(?P<email_category>[\w]+)/(?P<email_reason>[\w]+)/$', 'emails.views.EmailsHTML'),

	url(r'^account/login/admin/$', 'login.views.AdminLogin'),
	#url(r'^account/login/hello/$', 'adminweb.views.Console'),
	
	#url(r'^user/agreement/$', 'signup.views.Agreement'),
	

	url(r'^developers/(?P<path>.*)$', 'wot.views.Proxy', {'target_url': 'http://ru.wargaming.net/developers/'}),
	url(r'^id/(?P<path>.*)$', 'wot.views.Proxy', {'target_url': 'http://ru.wargaming.net/id/'}),	
	
	url(r'^adv/(?P<campaign>.*)/(?P<add_group>.*)/$', 'views.views.Advertisement'),
	
	# Dajaxice required
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
# Dajaxice required, but I'm not sure if I need this too
urlpatterns += staticfiles_urlpatterns()
