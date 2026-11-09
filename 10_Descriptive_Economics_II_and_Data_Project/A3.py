import pandas as pd
import matplotlib.pyplot as plt
from dstapi import DstApi

columns_dict = {'TRANSAKT': 'variable', 'PRISENHED': 'unit', 'TID': 'year', 'INDHOLD': 'value'}

var_dict = {
    'P.31 Household consumption expenditure': 'C',
    'P.31 Non-profit institutions serving households (NPISH) consumption expenditure': 'C',
    'P.3 Government consumption expenditure': 'G',
    'P.5 Gross capital formation': 'I',
    'P.6 Export of goods and services': 'X',
    'P.7 Import of goods and services': 'M',
}

unit_dict = {'2020-prices, chained values': 'real', 'Current prices': 'nominal'}


def national_accounts():
    """Download NAH1, keep C, G, I, X, M in current prices, one column per variable."""

    # a. download the whole table
    api = DstApi('NAH1')
    params = api._define_base_params(language='en')
    nah1 = api.get_data(params=params)

    # b. short names
    nah1 = nah1.rename(columns=columns_dict)
    nah1['variable'] = nah1['variable'].replace(var_dict)
    nah1['unit'] = nah1['unit'].replace(unit_dict)

    # c. keep what we need
    I = nah1['variable'].isin(['C', 'G', 'I', 'X', 'M']) & (nah1['unit'] == 'nominal')
    nah1 = nah1.loc[I].copy()
    nah1['value'] = nah1['value'].astype(float)

    # d. households + NPISH -> one C per year, then wide
    nah1 = nah1.groupby(['variable', 'year'], as_index=False)['value'].sum()
    wide = nah1.pivot_table(index='year', columns='variable', values='value')
    return wide


def shares(wide):
    """GDP from the expenditure side, and the shares of its components."""

    wide = wide.copy()
    wide['Y'] = wide['C'] + wide['G'] + wide['I'] + wide['X'] - wide['M']
    wide['C_share'] = wide['C']/wide['Y']*100
    wide['I_share'] = wide['I']/wide['Y']*100
    wide['NX_share'] = (wide['X'] - wide['M'])/wide['Y']*100
    print(wide[['C_share', 'I_share', 'NX_share']].tail().round(1))

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(wide.index, wide['C_share'], label='Private consumption')
    ax.plot(wide.index, wide['I_share'], label='Investment')
    ax.plot(wide.index, wide['NX_share'], label='Net exports')
    ax.axhline(0.0, color='black', linewidth=0.8)
    ax.set_xlabel('Year')
    ax.set_ylabel('Percent of GDP')
    ax.legend()
    fig.tight_layout()
    plt.show()
    return wide
