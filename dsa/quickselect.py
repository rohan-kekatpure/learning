from random import randint
import  matplotlib.pyplot as pl
import numpy as np


def quickselect(arr, k):
    if len(arr) == 1:
        return arr[0]

    pivot = arr[-1]
    lows = [e for e in arr if e < pivot]
    highs = [e for e in arr if e > pivot]
    pivots = [e for e in arr if e == pivot]

    if k < len(lows):
        return quickselect(lows, k)
    elif k < len(lows) + len(pivots):
        return pivots[0]
    else:
        return quickselect(highs, k - len(lows) - len(pivots))

def quickselect_median(arr):
    n = len(arr)
    if n % 2 == 1:
        return quickselect(arr, n // 2)
    else:
        a = quickselect(arr, n // 2 - 1)
        b = quickselect(arr, n // 2)
        return 0.5 * (a + b)

def main():
    arr = [1, 1, 1, 1, 1, 1]
    print(quickselect_median(arr))
    print(np.median(arr))

if __name__ == '__main__':
    scaling_study()

    

