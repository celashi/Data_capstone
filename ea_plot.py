# -*- coding: utf-8 -*-

import pandas as pd
from statsmodels.stats.api import anova_lm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

def main_effects(df:pd.DataFrame, factors:list, response:str) -> pd.Series:
    '''
    Calculate the effect size of main factors

    Parameters
    ----------
    df : pandas.dataframe
        data frame containing the experimental design with factors and response.
    factors : list(str)
        list of factors as strings. Used to index the data frame at the correct
        spot.
    response : str
        name of the response variable. Used to index the data frame at the
        correct spot.

    Returns
    -------
    pandas.Series
        Pandas series with effect size relative to the mean for each level of
        each factor

    '''
    # Get dummy variables and empty series for results
    dummies = pd.get_dummies(df, columns=factors)
    eff = pd.Series(index=dummies.columns, name='Effect size', dtype=float)
    # Iterate through factors then levels to calculate effect size
    for i in factors:
        for j in df[i].unique():
            eff[f'{i}_{j}'] = sum(dummies[f'{i}_{j}'] *
                                  dummies[response]/dummies[f'{i}_{j}'].sum())
    # return the series with nan dropped
    return eff.dropna()


def maineffectsplot(df:pd.DataFrame, factors:list, response:str) -> plt.figure:
    '''
    Plot the effect size of the main factors

    Parameters
    ----------
    df : pandas.dataframe
        data frame containing the experimental design with factors and response.
    factors : list(str)
        list of factors as strings. Used to index the data frame at the correct
        spot.
    response : str
        name of the response variable. Used to index the data frame at the
        correct spot.

    Returns
    -------
    matplotlib.figure
        Figure object to manipulate after creating the plot.

    '''
    # Calculate the main effects
    maineffect = main_effects(df, factors, response)
    # Set up subplots for each factor
    fig, ax = plt.subplots(1, len(factors), sharey=True)
    # Iterate through the subplots and plot effect on appropriate plot
    for i, j in enumerate(ax):
        levels = df.loc[:, factors[i]].unique()
        j.plot(
            levels, maineffect.loc[f'{factors[i]}_{levels[0]}':
                                   f'{factors[i]}_{levels[-1]}'],'o-')
        j.set_xticks(levels)
        j.set_xlabel(factors[i])
        if i == 0:
            j.set_ylabel(response)

    fig.tight_layout()
    return fig

datas = pd.read_excel('Data.xlsx', sheet_name='Sheet3')
fig = maineffectsplot(datas, ['Mass of sugar (g)','Fermentation temperature (°C)'], 'Bubble count')
ax = fig.get_axes()
ax[0].set_ylabel('Bubble count')
ax[0].set_xlabel('Mass of sugar (g)')
ax[1].set_xlabel('Fermentation temperature (°C)')
#fig.suptitle('Main Effects Plot')
fig.savefig('fig1.png',dpi=300,format='png')