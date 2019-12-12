/* Must include Python.h before any standard headers*/
#include <Python.h>
#include "fact.h"
static PyObject* wrap_fact(PyObject *self, PyObject *args)
{
    /* Python->C data conversion */
    int n, result;
    // the string i here means there is only one integer
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    
    /* C Function Call */
    result = fact(n);
    
    /* C->Python data conversion */
    return Py_BuildValue("i", result);
}

/* Method table declaring the names of functions exposed to Python*/
static PyMethodDef ExampleMethods[] = {
    {"fact",  wrap_fact, METH_VARARGS, "Calculate the factorial of n"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

/* Module initialization function called at "import example"*/
PyMODINIT_FUNC 
initexample(void)
{
    (void) Py_InitModule("example", ExampleMethods);
}
