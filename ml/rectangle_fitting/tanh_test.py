import numpy as np
import matplotlib.pyplot as pl

def iterfunc(b0, s_, ct, dt):
    b = b0
    for _ in range(10):
        print(b)
        t1 = s_ * (dt - b)
        t2 = 1. - np.tanh(t1)
        t3 = 1. - t2 / ct
        b = np.arctanh(t3) / s_

if __name__ == '__main__':
    DT = 5.0
    CT = 0.8
    s = 1.0
    beta_0 = DT
    iterfunc(beta_0, s, CT, DT)
