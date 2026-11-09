import numpy as np
import pandas as pd


def decile_shares(seed=2026, N=10_000, sigma=0.6):
    """Income share of each decile for simulated log-normal incomes."""

    rng = np.random.default_rng(seed)
    df = pd.DataFrame({'inc': np.exp(rng.normal(0.0, sigma, size=N))})

    # a. decile groups: 10 groups with the same number of people
    df['decile'] = pd.qcut(df['inc'], 10, labels=range(1, 11))

    # b. share of total income in each decile
    shares = df.groupby('decile', observed=True)['inc'].sum()/df['inc'].sum()
    print('Income share by decile:')
    print(shares.round(3))
    print(f'Sum of shares: {shares.sum():.3f}')

    # c. the same top-10 share from decile averages (the data project's formula)
    means = df.groupby('decile', observed=True)['inc'].mean()
    print(f'Top 10 pct. share from sums:  {shares.loc[10]:.4f}')
    print(f'Top 10 pct. share from means: {means.loc[10]/means.sum():.4f}')
    return shares
