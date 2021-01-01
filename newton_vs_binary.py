#!/usr/bin/env python3

import sys
import os
import itertools as it
import numpy as np
import pandas as pd
from scipy import linalg
from scipy.stats import norm
from decimal import *

f = lambda x: x**3 - Decimal(10)
df = lambda x: Decimal(2) * x**2
NUM_DIGITS=10
x0 = Decimal(1.)
solution = Decimal(10)**Decimal(1/3)
a0, b0 = Decimal(0.), Decimal(12.)

def run_newton(f, df, x0, num_iter=NUM_DIGITS):
    xk = x0
    history = [x0]
    for k in range(num_iter):
        xk -= f(xk) / df(xk)
        history.append(xk)
    return history


def run_binary(f, a, b, num_iter=NUM_DIGITS):
    history = []

    for k in range(num_iter):
        med = a/2 + b/2
        history.append({'a': a, 'b': b, 'med': med})
        if f(med) > 0:
            b = med
        else:
            a = med

    history.append({'a': a, 'b': b, 'med': med})
    return list(zip(*[(h['a'], h['b'], h['med']) for h in history]))

def num_trailing_zeros(x):
    return int(np.log(float(x)))

xks_newton = run_newton(f, df, x0)
_, _, xks_binary = run_binary(f, a0, b0)

pd.DataFrame([xks_newton, xks_binary], index=["newt", "bin  "]).astype(float).T.plot()

pd.DataFrame([list(map(num_trailing_zeros, abs(np.array(L) - solution))) for L in (xks_newton, xks_binary)], index=["newt", "bin"]).T.plot()
