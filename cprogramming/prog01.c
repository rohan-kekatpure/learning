#include <stdio.h>    

double my_var = 2.0;

int fact(int n) {
    if (n == 1) {
        return 1;
    }

    return n * fact(n - 1);
}

