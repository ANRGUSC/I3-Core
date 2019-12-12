import jwt
import datetime
original_claim = {
    'iss': 'ANRG',
    # The time that the token was issued at
    'iat': datetime.datetime.utcnow(),
    # The time the token expires.
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
    # The audience field should always be set to the I3 device id.
}
print '\noriginal claim : a Json object\n'
print original_claim

with open('/home/zxc/Desktop/private2.pem', 'r') as f:
    private_key = f.read()
   
signature = jwt.encode(original_claim, private_key, algorithm = 'RS256')

print signature

'''
Below token is valid until 03/01/2019

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBTlJHIiwiaWF0IjoxNTUxMjEwNzQwLCJleHAiOjE1NTE1NzA3NDB9.HkNftmSqRuZFtjnwP5h37CBnaeOsVOReVpfNjHz575PUyXkP1kJ8-NJyNp_TvJs7FtbXrGWIepOMeIAS80wfRPjdRSaFpifNbPAB3Vyw7FPslyu7Uv_VdEIFM3Tf19iapH8WdHNV3PQpcRIDpF9GPNWrxSlfJucmOzQd8KtgazRP4e-aq38jJCJSiZlUHEwJFCFZ5nwySeaRup1McPkTm7b-SCbIidLOqb0_53fytlqKdlIYA2qZTqNQgyM9zE8NDupjPNizFm5nh3yXVxzl-SLUydZ4mhMYLgVYByR40-QNeaY7acKRTj33xDbxlGTDghyUdjnFm1RasArJUQ3F0w

Its public key string

MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArBrK2Lj8ALUzBc3tsIcbbx9MmRvXmPGJBKFiYZVL1i4bH6I+qoGhxcxhqh6+iSuDCmEVL+OU8H4YrQLgYWmH4PR39SL2FicuLRcSIG32zow7ji5utzTA/NVVJ1Rqe5TNy7aIy1BDd3Os/j1cxJQs+ypqEgNl1NgUgp+lf0+CHcketDlSp0PmFvncdc9MtfOPEwaacOyBw2UC+ni77ncFYzRsz3h+e/xIfvB6rQak9D7lzzQulVU84Iz2G/OgCvLn5566uyQ7l3gC3b9jNkA63lfNR0jYNvxo0O9GBAhDIYn0NI8n5TNzf5JOFCuma1E6hM/HM/FkKktMxBWR+lStxQIDAQAB

'''
