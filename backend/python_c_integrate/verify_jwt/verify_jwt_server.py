import jwt
#import sys
'''
# encode
original_claim = {
    'iss': 'ANRG',
    # The time that the token was issued at
    'iat': datetime.datetime.utcnow(),
    # The time the token expires.
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    # The audience field should always be set to the I3 device id.
}
print '\noriginal claim : a Json object\n'
print original_claim

with open('/home/zxc/Desktop/private2.pem', 'r') as f:
    private_key = f.read()
   
signature = jwt.encode(original_claim, private_key, algorithm = 'RS256')
print '\nsignature : (orininal claim digitally signed by private key)\n'
print signature
'''
# NOTE: the signature has an auto expire time, so generate a new one for every test
'''
a possible signature:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBTlJHIiwiaWF0IjoxNTUwODgwMjk2LCJleHAiOjE1NTA4ODM4OTZ9.TUkBDspO7qimM7Uugk8hyJuMK2LYQtCMo3RGzDgN1rb_WmtrrYMge38g1glqZ6qvFzswt68EZCYxAz0DDluU0hsypuEYcEmGAQBJXbFEF-cdNxCt6s6tgaq62QY1W7dzWWLoKOV279CkMXierAWQOvkjCs3tRZPuWwcsMKdjGWXXGoYK2B-TtEUCWkovsFXVUVwLLo4sHzcktUi5uAwAAD0pEQqgOz3yZ5zttZbbcRAzZRW4Qy_jFOdAHCiOpjBj8PbfDqIxVPUgPICrvaaF6qbzPN_GF3sKqb1crOwqkVsN4lypkxUYKy3ltQ8D6sOSfiK8abyfBhGxNGeaAKjweA
'''

# public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArBrK2Lj8ALUzBc3tsIcbbx9MmRvXmPGJBKFiYZVL1i4bH6I+qoGhxcxhqh6+iSuDCmEVL+OU8H4YrQLgYWmH4PR39SL2FicuLRcSIG32zow7ji5utzTA/NVVJ1Rqe5TNy7aIy1BDd3Os/j1cxJQs+ypqEgNl1NgUgp+lf0+CHcketDlSp0PmFvncdc9MtfOPEwaacOyBw2UC+ni77ncFYzRsz3h+e/xIfvB6rQak9D7lzzQulVU84Iz2G/OgCvLn5566uyQ7l3gC3b9jNkA63lfNR0jYNvxo0O9GBAhDIYn0NI8n5TNzf5JOFCuma1E6hM/HM/FkKktMxBWR+lStxQIDAQAB\n-----END PUBLIC KEY-----"

def verify_jwt_1(signature, public_key):
	decoded_signature = {}
	try:
		decoded_signature = jwt.decode(signature, public_key, algorithm = 'RS256')
	except jwt.exceptions.InvalidSignatureError:
		print('jwt.exceptions.InvalidSignatureError')
		return 0
	except jwt.exceptions.ExpiredSignatureError:
		print('Signature has expired')
		return 0
	except ValueError:
		print('ERROR!')
		return 0
	
	print('decode successful, matched!')
	print(decoded_signature)
	return 1

# It's best if we store just a string for public key in MySQL
# However, pyjwt requires a specific public key format
# which contains space, and cannot be used as commend line args
# so, take in the string from backend, and make it compatible with key format

def generate_public_key_from_string(t):
	public_key = ""
	public_key += "-----BEGIN PUBLIC KEY-----\n"
	public_key += t
	public_key += "\n-----END PUBLIC KEY-----"
	return public_key

# pass two commend line args
# argv[1] is signature, argv[2] is public_key string (not in key format)	
# let users be responsible for storing the public key correctly:
# delete all enters
# delete "-----BEGIN PUBLIC KEY----" and "-----END PUBLIC KEY-----"
'''
if __name__=="__main__":
	print 'FINAL RESULT\n'
	print sys.argv[1]
	print sys.argv[2]
	signature = sys.argv[1]
	public_key = generate_public_key_from_string(sys.argv[2])
	# return value: 0 for unmatched, 1 for matched
	print verify_jwt_1(signature, public_key)
'''
# the interface function that another c program should call
# input: 2 strings from c program
# s stands for signature, t stands for public key string
def python_c_interface(s, t):
	return verify_jwt_1(s, generate_public_key_from_string(t))
	
