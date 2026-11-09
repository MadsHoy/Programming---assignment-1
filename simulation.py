
import numpy as np

def simulate(shares, medians, N=10000, seed=42):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0, 1, size=N)

    ages = np.zeros(N, dtype=int)
    wealth = np.zeros(N)

    lower = 0

    for j, share in enumerate(shares):
        upper = lower + share
        mask = (u >= lower) & (u < upper)

        ages[mask] = j
        wealth[mask] = medians[j]

        lower = upper

    return ages, wealth

def simulate_wealth(ages, values, seed=42):
    rng = np.random.default_rng(seed)
    ranks = rng.integers(1, 100, size=len(ages))

    wealth = np.zeros(len(ages))

    for i, r in enumerate(ranks):
        wealth[i] = values[ages[i], r - 1]

    return wealth



def simulate_distribution(shares, values, N=10000, seed=42):
    rng = np.random.default_rng(seed)

    # Draw age groups
    u = rng.uniform(0, 1, size=N)
    ages = np.zeros(N, dtype=int)

    lower = 0
    for j, share in enumerate(shares):
        upper = lower + share
        ages[(u >= lower) & (u < upper)] = j
        lower = upper

    # Draw percentile ranks and assign wealth
    ranks = rng.integers(1, 100, size=N)
    wealth = np.zeros(N)

    for i, r in enumerate(ranks):
        wealth[i] = values[ages[i], r - 1]

    return ages, wealth

