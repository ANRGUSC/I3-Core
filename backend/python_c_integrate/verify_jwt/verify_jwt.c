#include"Python.h"
#include<stdio.h>
//#define PYTHON_JWT_PATH "/home/zxc/Desktop/python_c_integrate/"

/* Linux compile command:
 * export PYTHONPATH=.:$PYTHONPATH
 * gcc verify_jwt.c -o verify_jwt -I/usr/include/python2.7/ -lpython2.7
 */
 
int verify_jwt_from_python(char* signature, char* public_key_string) {

	Py_Initialize();     
	if (!Py_IsInitialized())         
		return -1;
	PyRun_SimpleString("import sys\n");
	PyRun_SimpleString("print 'check_point_1'");
	PyRun_SimpleString("sys.path.append(\"/home/zxc/Desktop/python_c_integrate/verify_jwt\")");
	PyRun_SimpleString("print 'check_point_2'");
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
	 * DON'T run this in mosquitto compliation, auth-plugin compliation etc.
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
	PyTuple_SetItem(pArgs,0, PyString_FromString(signature));
	PyTuple_SetItem(pArgs,1, PyString_FromString(public_key_string));
	pRetVal = PyObject_CallObject(pFunc, pArgs);
	flag = PyInt_AsLong(pRetVal);
	
	Py_DECREF(pArgs);
	Py_DECREF(pModule);
	Py_DECREF(pRetVal);
    
	Py_Finalize();
    
	return flag;
}
/*
	pModule = PyImport_Import(PyString_FromString("verify_jwt"));
	
	pFunc = PyObject_GetAttrString(pModule, "python_c_interface"); 

	pArgs = PyTuple_New(2);
	PyTuple_SetItem(pArgs,0, PyString_FromString(signature));
	PyTuple_SetItem(pArgs,1, PyString_FromString(public_key_string));

	pValue = PyObject_CallObject(pFunc, pArgs);
  
	flag = PyInt_AsLong(pValue);
	return flag;
*/

/*

a possible signature:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBTlJHIiwiaWF0IjoxNTUwODgwMjk2LCJleHAiOjE1NTA4ODM4OTZ9.TUkBDspO7qimM7Uugk8hyJuMK2LYQtCMo3RGzDgN1rb_WmtrrYMge38g1glqZ6qvFzswt68EZCYxAz0DDluU0hsypuEYcEmGAQBJXbFEF-cdNxCt6s6tgaq62QY1W7dzWWLoKOV279CkMXierAWQOvkjCs3tRZPuWwcsMKdjGWXXGoYK2B-TtEUCWkovsFXVUVwLLo4sHzcktUi5uAwAAD0pEQqgOz3yZ5zttZbbcRAzZRW4Qy_jFOdAHCiOpjBj8PbfDqIxVPUgPICrvaaF6qbzPN_GF3sKqb1crOwqkVsN4lypkxUYKy3ltQ8D6sOSfiK8abyfBhGxNGeaAKjweA

its public_key_string:
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArBrK2Lj8ALUzBc3tsIcbbx9MmRvXmPGJBKFiYZVL1i4bH6I+qoGhxcxhqh6+iSuDCmEVL+OU8H4YrQLgYWmH4PR39SL2FicuLRcSIG32zow7ji5utzTA/NVVJ1Rqe5TNy7aIy1BDd3Os/j1cxJQs+ypqEgNl1NgUgp+lf0+CHcketDlSp0PmFvncdc9MtfOPEwaacOyBw2UC+ni77ncFYzRsz3h+e/xIfvB6rQak9D7lzzQulVU84Iz2G/OgCvLn5566uyQ7l3gC3b9jNkA63lfNR0jYNvxo0O9GBAhDIYn0NI8n5TNzf5JOFCuma1E6hM/HM/FkKktMxBWR+lStxQIDAQAB

unmatched public_key_string:
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3FhyKLFV09e6v/LBWf1iCptCry2Amx8NkLi6T39gXeA9s0u8CsWMfcnbqlcaOV/239ckrJtZ5hgCf98ErNRfl3MdkzWuoRqILZYQZIlHE9gXmAbjCb6cNBs7zjmb7lPlhp6IEwWB85Rq8vkEPCYINZmpFIk6nDy/Q9G8P5oE3+xKipy43d47dYuIa9fQlHpjfV1rCbE+n0OVTB1/a8/v/oL1NMDVznuJM9mHR8+mBVJLdxPSxjyLjzO3b3M641WWmzXwnYgUtSrzEMjgmr6J6l+TQ0xC3g68TO/OaVsoJCUJs1c+qGHPVzkRZ3sxBsDESoKuRfSWQYuU/XWEw6Lr1QIDAQAB

*/

int main(int argc, char** argv) {
	//system("echo ${pwd}");
	//system("export PYTHONPATH= pwd:$PYTHONPATH");
	printf("\n%d\n", verify_jwt_from_python(argv[1], argv[2]));
	return 0;
}
