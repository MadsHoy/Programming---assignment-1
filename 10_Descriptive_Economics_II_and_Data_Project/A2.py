import pandas as pd
import matplotlib.pyplot as plt


def load_and_merge(emp_file='data/RAS200.csv', inc_file='data/INDKP101.csv'):
    """Unemployed share by year, and the merge with income."""

    emp = pd.read_csv(emp_file)
    inc = pd.read_csv(inc_file)
    emp['unemp_share'] = emp['part_rate'] - emp['emp_rate']

    # a. average across municipalities by year
    by_year = emp.groupby('year')['unemp_share'].mean()
    print(f'Highest average unemployed share: {by_year.max():.2f} percent in {by_year.idxmax()}')

    # b. merge, and what is lost
    merged = pd.merge(emp, inc, on=['municipality', 'year'], how='inner', validate='1:1')
    lost = sorted(set(emp['municipality']) - set(merged['municipality']))
    print(f'Rows: emp {emp.shape[0]}, merged {merged.shape[0]}; municipalities lost: {lost}')
    return merged


def quartiles_2023(merged):
    """Unemployed share by income quartile in 2023."""

    data = merged.loc[merged['year'] == 2023].copy()
    data['quartile'] = pd.qcut(data['inc'], 4, labels=[1, 2, 3, 4])
    print('Average unemployed share by income quartile, 2023 (1 = poorest):')
    print(data.groupby('quartile', observed=True)['unemp_share'].mean().round(2))
    print(f"Correlation of unemployed share and income: {data[['unemp_share', 'inc']].corr().iloc[0, 1]:.2f}")


def quartiles_all_years(merged):
    """Optional: quartiles within each year, and the path over time."""

    merged = merged.copy()
    merged['quartile'] = merged.groupby('year')['inc'].transform(lambda s: pd.qcut(s, 4, labels=False) + 1)
    table = merged.groupby(['year', 'quartile'])['unemp_share'].mean().unstack()

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(1, 1, 1)
    for q in table.columns:
        ax.plot(table.index, table[q], label=f'income quartile {q}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Unemployed share (%)')
    ax.set_title('Poorer municipalities, more unemployment')
    ax.legend()
    fig.tight_layout()
    plt.show()
