#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from twilio.rest import TwilioRestClient 
import phone_numbers

# put your own credentials here 
ACCOUNT_SID = "ACCOUNT_SID_GOES_HERE" 
AUTH_TOKEN = "ACCOUNT_AUTH_TOKEN_GOES_HERE" 
 
text = "Please respond with this code in your Telegram session to continue: %s"



def two_factor_authenticate(token, uid):
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	number = phone_numbers.directory[uid]
	number = number.strip()
	number = "+972" + number
	client.messages.create(
		to=number,
		from_="PUT_HERE_YOUR_ASSIGNED_TWILIO_NUMBER",
		body=text % token, )
