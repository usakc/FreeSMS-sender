
class SMS:
	"""Object representation of SMS message"""
	toNum = ""			# recipient number
	text = ""  			# SMS text
	gateway = "" 		# gateway name
	captchaCode = None 	# captcha code
	error = "" 			# error while sending

	