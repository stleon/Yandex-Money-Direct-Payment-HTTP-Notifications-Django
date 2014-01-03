Yandex Money
=============
Yandex Money (http://money.yandex.ru/eng/) offers you to implement payments-online services based on cyber-currency 'yandex money' in your internet-projects.
These money could be landed to credit cards and bank accounts directly.

Direct Payment 
================
Yandex Money offers you Direct Payment service that allows you create click-to-buy ready-to-go buttons and iframes.
(https://money.yandex.ru/embed/)

HTTP Notifications  
====================
Direct Payment (http://api.yandex.com/money/doc/dg/reference/notification-p2p-incoming.xml) can send you HTTP Notifications for each payment received via your click-to-buy button.
This Python code can process such Notifications and send data further to your application.

for Django
======================================
Django (https://www.djangoproject.com) - is a great web-framework based on Python, that allows to easily build essential solutions.

we use
==========
This code is used in our projects for receiving and processing funds via Yandex Money. We constantly improve and support this code and going forward with other Yandex Money services.
And we hope this code could be usefull both for Django and Python developers with their application services based on Yandex Money.

How it works
=============
Yandex.Money sends an HTTP Notiication to your server in case of incoming funds to your Yandex.Money purse. This code process this HTTP Notification, logs it into DB, checks HASH validity and then calls Credit(**kwargs) function to land money to your system

Folders
---------
1. *project* folder - is your Django project folder name
2. *billing* and *commons* folders - are your Django apps folders, both billing and commons apps are listed in project/settings.py APPLICATIONS section

Setup
-----
We do not provide automatic setup for this code, because billing system setup is quite an intimate thing and requires lots of adjustments and look-through code things, so, we hope you will get the only things and ideas you need from our open-sourse code, but not the all files without single change

Items to adjust
----------------
1. *ADMINS* section in project/settings.py
2. *NOTIFICATION_SECRET* variable in billing/Yandex/model_directpayment.py

