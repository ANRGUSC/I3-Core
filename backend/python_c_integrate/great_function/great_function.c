#include <Python.h>

// convert commend line arg string to int
int string_to_int(char* s) {
	int sum = 0;
	int size = 0;
	for(int i=0; s[i]!='\0'; i++)
		size++;
	int t = 1;	
	for(int i=size-1; i>=0; i--) {
		sum += t * (s[i] - '0');
		t *= 10;
	}
	return sum;
}

char* great_function_from_python(char* a, char* b) {
    char* res;
    PyObject *pModule,*pFunc;
    PyObject *pArgs, *pValue;
    /* import */
    pModule = PyImport_Import(PyString_FromString("great_module"));
    /* great_module.great_function */
   /*============================================
    *     export PYTHONPATH=.:$PYTHONPATH
    *  IS REQUIRED IN BASH BEFORE COMPILATION
    *============================================
    */
    pFunc = PyObject_GetAttrString(pModule, "great_function"); 
    /* build args */
    pArgs = PyTuple_New(2);
    PyTuple_SetItem(pArgs,0, PyString_FromString(a));
    PyTuple_SetItem(pArgs,1, PyString_FromString(b));
    /* call */
    pValue = PyObject_CallObject(pFunc, pArgs);
    res = PyString_AsString(pValue);
    return res;
}

int main(int argc, char **argv) {
    Py_Initialize();
	printf("argc: %d\n", argc);
	printf("argv[1], argv[2]: %s, %s",argv[1], argv[2]);
    //int temp1 = string_to_int(argv[1]);
	//int temp2 = string_to_int(argv[2]);
    printf("\nfinal result: %s\n",great_function_from_python(argv[1], argv[2]));
    Py_Finalize();
}

