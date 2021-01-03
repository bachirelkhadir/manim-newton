#!/usr/bin/env python3

f = lambda x: (x**4/4 - 2*x)/5. + 1
df = lambda x: (x**3 - 2)/5.
ddf = lambda x: 2*x**2

quad_f = lambda x: (lambda y: f(x) + df(x) * (y - x) + 1/2 * (y-x)**2 * ddf(x))

f_str = r"f(x) = \frac1{20} x^4 - \frac 25 x + 1"

NUM_DIGITS=30
x0 = -0.5
