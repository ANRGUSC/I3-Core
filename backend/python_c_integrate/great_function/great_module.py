import jwt
#def great_function(s, t):
#    return s + t

def great_function(signature, public_key):
	#decoded_signature = {}
	#try:
	pk = ""
	pk += "-----BEGIN PUBLIC KEY-----\n"
	pk += public_key
	pk += "\n-----END PUBLIC KEY-----"
	decoded_signature = jwt.decode(signature, pk, algorithm = 'RS256')
	#except jwt.exceptions.InvalidSignatureError:
	#	print 'jwt.exceptions.InvalidSignatureError'
	#	return 0
	#except ValueError:
	#	print 'ERROR!'
	#	return 0
	
	#print 'decode successful, matched!'
	print '\n\ndecode signature\n\n'
	print decoded_signature
	print '\n\ndecode signature\n\n'
	return pk

