# -*- coding: utf-8 -*-
"""O2 CZ free gateway can be used to sending sms to O2 CZ"""

import urllib, urllib2
import re
import cookielib
from BaseGateway import *

from data.SMS import *

class Gateway(BaseGateway):
	def __init__(self, delegate):
		BaseGateway.__init__(self, delegate)
		self.opener.addheaders.append( ('Referer', 'http://sms.1188.cz/'))

	@classmethod
	def getName(cls):
		return "O2 CZ"

	def getMaxLength(cls):
		return 60

	def _asyncSend(self, sms):
		if sms.captchaCode == None:
			#download captcha
			sms.captchaCode = None
			respStr = self.opener.open("http://www.google.com/recaptcha/api/challenge?k=6LfFmc8SAAAAAKZS7BmYx4cEys7zo1y_LYHgxZ5o&ajax=1&cachestop=0.3157223965972662").read()
			match = re.findall(" challenge : '(.*?)',", respStr, re.DOTALL)
			self.challange = match[0].strip()
			sms.captchaImageData = self.opener.open('http://www.google.com/recaptcha/api/image?c='+self.challange).read()
			self.delegate.showCaptcha(sms)
			while sms.captchaCode == None: #waiting until the user fills captcha
				pass
			if sms.captchaCode == "cancel": # sending was canceled
				sms.error = "SMS nebyla odeslána!"
				self.delegate.setSMSNotSent(sms)
				return
			else: # resend SMS with filled captcha
				self.sendSMS(sms)
		else:
			postData = urllib.urlencode({'sms[phone_numbers][]' : sms.toNum, 'sms[text]' : sms.text, 'recaptcha_challenge_field' : self.challange, 'recaptcha_response_field' : sms.captchaCode})
			respStr = self.opener.open('http://sms.1188.cz/sms', postData).read()
			#check if message was successfully sent
			match = re.search("SMS přijata", respStr)
			if match:
				self.delegate.setSMSSent(sms)
				return

			#look for bad captcha
			match = re.search("text zadán chybně", respStr)
			if match:
				sms.captchaCode = None
				self.sendSMS(sms)
				return
			
			#look for possible error messages
			match = re.findall('<div class="error_message">([\s\S]*?)<\/div>', respStr, re.DOTALL)
			if match:
				error = ",".join(match)
				sms.error = error
				self.delegate.setSMSNotSent(sms)
				return
			
			
		

		
