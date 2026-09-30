"""
How often does peeking at an A/A test crown a fake winner?

Both variants convert at exactly 10%, so any "significant" result is a false positive.
We compare two strategies over 2,000 simulated experiments:
  1. Peek every 25 visitors per variant (from n=200) and stop at the first p < 0.05.
  2. Look once, at the planned sample size.

Run:  python peeking_simulation.py
"""
import numpy as np
from scipy.stats import norm  # only for the normal CDF

RATE, N, STEP, START, SIMS, SEED = 0.10, 6000, 25, 200, 2000, 42
rng = np.random.default_rng(SEED)

peeks = np.arange(START, N + 1, STEP)
a = np.cumsum(rng.random((SIMS, N)) < RATE, axis=1)[:, peeks - 1]
b = np.cumsum(rng.random((SIMS, N)) < RATE, axis=1)[:, peeks - 1]

pooled = (a + b) / (2 * peeks)
se = np.sqrt(2 * pooled * (1 - pooled) / peeks)
z = (b / peeks - a / peeks) / se
p = 2 * (1 - norm.cdf(np.abs(z)))

peeking = (p < 0.05).any(axis=1).mean()
one_look = (p[:, -1] < 0.05).mean()

print(f"Peek every {STEP} visitors, stop at first p < 0.05: {peeking:.1%} fake winners")
print(f"Look once at n = {N:,}:                              {one_look:.1%} fake winners")
