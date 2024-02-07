#include<iostream>
#include<pybind11/pybind11.h>

int add(int x, int y) {
    return x + y;
}

int sub(int x, int y) {
    return x - y;
}

int mul(int x, int y) {
    return x * y;
}

int divide (int x, int y) {
    if (y != 0) {
        return x / y;
    } else {
        return 0;
    }
}


PYBIND11_MODULE(hellolib, m){
    m.doc() = "Arithmetic operations";
    m.def("add", &add, "Add two integers");    
    m.def("sub", &sub, "Subtract two integers");    
    m.def("mul", &mul, "multiply two integers");    
    m.def("div", &divide, "divide two integers");        
}