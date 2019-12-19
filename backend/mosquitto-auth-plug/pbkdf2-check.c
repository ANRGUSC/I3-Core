/*
 * Copyright (c) 2013 Jan-Piet Mens <jp@mens.de>
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of mosquitto nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include "base64.h"
//#define PYTHON_JWT_PATH ${PATH_TO_YOUR_VERIFY_JWT_PYTHON}

#define SEPARATOR       "$"
#define TRUE	(1)
#define FALSE	(0)


/*
 * Split PBKDF2$... string into their components. The caller must free()
 * the strings.
 */

static int detoken(char *pbkstr, char **sha, int *iter, char **salt, char **key)
{
	// WHAT AN AUTHENTICATION STRING LOOKS LIKE:
	// PBKDF2$sha256$901$QQPufrr6pT0mlsTX$2RJqXfmP5Nz8u6stbDj48Zvs2WgSOn4W
	
	// if any of the conditions is not met
	// return rc = 1, meaning invalid
	// if all conditions are met
	// return rc = 0
	char *p, *s, *save;
	int rc = 1;

	save = s = strdup(pbkstr);
	// SEPARATOR : $
	// p is the part from s[0] to the element before '$'
	if ((p = strsep(&s, SEPARATOR)) == NULL)
		goto out;
	if (strcmp(p, "PBKDF2") != 0)
		goto out;
	// below: multiple $ signs indicating different info
	if ((p = strsep(&s, SEPARATOR)) == NULL)
		goto out;
	*sha = strdup(p);

	if ((p = strsep(&s, SEPARATOR)) == NULL)
		goto out;
	*iter = atoi(p);

	if ((p = strsep(&s, SEPARATOR)) == NULL)
		goto out;
	*salt = strdup(p);

	if ((p = strsep(&s, SEPARATOR)) == NULL)
		goto out;
	*key = strdup(p);

	rc = 0;

     out:
	free(save);
	return rc;
}

int pbkdf2_check(char *password, char *hash)
{
	char *sha, *salt, *h_pw;
	int iterations, saltlen, blen;
	char *b64, *keybuf;
	unsigned char *out;
	int match = FALSE;
	const EVP_MD *evpmd;
	int keylen, rc;
	
	/* This function takes in a credential from publishing script
	 * and an AUTHENTICATION string from backend
	 * the string is either an np-hashed password (for API key devices),
	 * or a plain text public key string (not a formal public key, but it will be parsed)
	 * first check if it starts with 'pbkdf2$shaxxx$...', this part is done by 'detoken'
	 * if the detoken fails, which means the backend auth string is not a vaild np-auth string
	 * go on to use it as a public key to decrypt (unsign) the password
	 * return 1 if it can be unsigned (decoded), 0 otherwise
	 * the jwt verification function is in python, and the c program is calling the python
	 * with a c-python interface (provided by <Python.h>)
	 */
	 
	/* Linux compile command:
	 * export PYTHONPATH=.:$PYTHONPATH
	 * gcc verify_jwt.c -o verify_jwt -I/usr/include/python2.7/ -lpython2.7
	 */
 	
 	// does the hash start with 'PBKDF2$sha'? if not, check public key
 	// 'hash' is the backend authentication string
 	
	// calculating string length
	int length = 0;
	int i;
	for(i=0; hash[i]!='\0'; i++)
		length++;
 	if(length <= 10)
 		return match;
 		
 	if(!(hash[0]=='P' && hash[1]=='B' && hash[2]=='K' && hash[3]=='D' && hash[4]=='F' && hash[5]=='2' && hash[6]=='$' && hash[7]=='s' && hash[8]=='h' && hash[9]=='a')) {
		
		Py_Initialize();     
		if (!Py_IsInitialized())         
			return -1;
		
		PyRun_SimpleString("import sys\n");
		PyRun_SimpleString("sys.path.append(\"/zxc/python_c_integrate/verify_jwt\")");
		PyRun_SimpleString("print sys.path");
		/* -1: wrong; 0: not match; 1: match */
		long flag = -1;
		PyObject *pModule, *pDict, *pFunc, *pArgs, *pRetVal;
		/* in below, it's not easy for this c program to find the path of "verify_jwt"
		 * even if they're in the same directory. if you don't write "if(!pModule)"
		 * then if .py script is not found, the system will have a 'core dumped' error
		 * and the whole system will break
		 * the "export PYTHONPATH=.:$PYTHONPATH" bash command is used to tell this c program
		 * where to look for the python script
		 * from my understanding, this is used to output the current working directory
		 * (which contains the verify_jwt.py) to a default PYTHONPATH (where PyImport looks
		 * for the script)
		 * DON'T run this command in mosquitto compliation, auth-plugin compliation etc.
		 * just use PyRun_SimpleString to append the verify_jwt.py dir to the py-c working dir
		 */
		pModule = PyImport_Import(PyString_FromString("verify_jwt_server"));

		if (!pModule) {
			printf("can't find py");
			getchar();
			return -1;
		}
		
		pDict = PyModule_GetDict(pModule);
		if (!pDict) {
			return -1;
		}
		
		pFunc = PyDict_GetItemString(pDict, "python_c_interface");
		if (!pFunc || !PyCallable_Check(pFunc)) {
			printf("can't find function");
			getchar();
			return -1;
		}
		
		pArgs = PyTuple_New(2);
		PyTuple_SetItem(pArgs,0, PyString_FromString(password));
		PyTuple_SetItem(pArgs,1, PyString_FromString(hash));
		pRetVal = PyObject_CallObject(pFunc, pArgs);
		flag = PyInt_AsLong(pRetVal);
	
		// Py_DECREF(pArgs);
		// Py_DECREF(pModule);
		// Py_DECREF(pRetVal);
		
		Py_Finalize();
		
		return flag;
	}
	
	if (detoken(hash, &sha, &iterations, &salt, &h_pw) != 0) {
		return match;
	}
	
	/* Determine key length by decoding base64 */
	if ((keybuf = malloc(strlen(h_pw) + 1)) == NULL) {
		fprintf(stderr, "Out of memory\n");
		return FALSE;
	}
	keylen = base64_decode(h_pw, keybuf);
	if (keylen < 1) {
		free(keybuf);
		return (FALSE);
	}
	free(keybuf);

	if ((out = malloc(keylen)) == NULL) {
		fprintf(stderr, "Cannot allocate out; out of memory\n");
		return (FALSE);
	}

#ifdef RAW_SALT
	char *rawSalt;

	if ((rawSalt = malloc(strlen(salt) + 1)) == NULL) {
		fprintf(stderr, "Out of memory\n");
		return FALSE;
	}

	saltlen = base64_decode(salt, rawSalt);
	if (saltlen < 1) {
		return (FALSE);
	}

	free(salt);
	salt = rawSalt;
	rawSalt = NULL;
#else
	saltlen = strlen((char *)salt);
#endif

#ifdef PWDEBUG
	fprintf(stderr, "sha        =[%s]\n", sha);
	fprintf(stderr, "iterations =%d\n", iterations);
	fprintf(stderr, "salt       =[%s]\n", salt);
	fprintf(stderr, "salt len   =[%d]\n", saltlen);
	fprintf(stderr, "h_pw       =[%s]\n", h_pw);
	fprintf(stderr, "kenlen     =[%d]\n", keylen);
#endif


	evpmd = EVP_sha256();
	if (strcmp(sha, "sha1") == 0) {
		evpmd = EVP_sha1();
	} else if (strcmp(sha, "sha512") == 0) {
		evpmd = EVP_sha512();
	}

	rc = PKCS5_PBKDF2_HMAC(password, strlen(password),
		(unsigned char *)salt, saltlen,
		iterations,
		evpmd, keylen, out);
	if (rc != 1) {
		goto out;
	}

	blen = base64_encode(out, keylen, &b64);
	if (blen > 0) {
		int i, diff = 0, hlen = strlen(h_pw);
#ifdef PWDEBUG
		fprintf(stderr, "HMAC b64   =[%s]\n", b64);
#endif
		
		/* "manual" strcmp() to ensure constant time */
		for (i = 0; (i < blen) && (i < hlen); i++) {
			diff |= h_pw[i] ^ b64[i];
		}

		match = diff == 0;
		if (hlen != blen)
			match = 0;

		free(b64);
	}

  out:
	free(sha);
	free(salt);
	free(h_pw);
	free(out);

	return match;
}

#if TEST
int main()
{
	char password[] = "password";
	char pbkstr[] = "PBKDF2$sha1$98$XaIs9vQgmLujKHZG4/B3dNTbeP2PyaVKySTirZznBrE=$2DX/HZDTojVbfgAIdozBi6CihjWP1+akYnh/h9uQfIVl6pLoAiwJe1ey2WW2BnT+";
	int match;

	printf("Checking password [%s] for %s\n", password, pbkstr);

	match = pbkdf2_check(password, pbkstr);
	printf("match == %d\n", match);
	return match;
}
#endif
