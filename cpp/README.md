### Wrapping C++ functions with Python `CMake` and `pybind11`

#### Introduction
Wrapping user-facing C++ functions with Python is a great way to enhance 
the ease-of-use of your library. Wrapping C/C++ code with Python is 
done in foundational libraries like Numpy and Scipy as well as ML and CV
libraries like Tensorflow and OpenCV. Earlier one needed to use Swig, Sip, 
or Boost.Python to wrap existing C/C++ code in Python. These all came 
with their limitations. Some could wrap only C code, while the other were 
flexible but difficult to use. 

Any library that enables wrapping of C/C++ code with Python must satisfy 
some basic requirements. It must not constrain the user to C only. That is
it must be able to wrap code with C++ classes at a minimum. Additionally, 
for numerical code, it should be able to map C/C++ arrays to numpy arrays.

[pybind11](https://pybind11.readthedocs.io/en/latest/index.html) is a modern
wrapper library that satisfies both constraints and is easy to use.

The present codebase shows a minimal example of wrapping C++ _functions_ and
exposing them as Python module level functions. We will later add wrapping of
C++ classes. 

#### Cmake
C or C++ code needs to be compiled into a machine-dependent binary executable 
file (aka _executable_). Two basic pieces of information need to be provided 
for generation of an executable: the _names_ of dependent functions and their
_code_. 

For example, assume that your C++ code uses an external library to compute the 
mean and standard deviation of a list of numbers. To create an executable the 
compiler will need names and signatures of the mean and the std dev functions.
Additionally, it will also need the compiled code of these functions. 



