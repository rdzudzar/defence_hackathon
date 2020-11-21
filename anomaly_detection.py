# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 12:11:00 2020

@author: Rob
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport
import numpy as np

from scipy import stats

# Scientific colormaps: https://cmasher.readthedocs.io/user/usage.html
import cmasher as cmr

plt.rcdefaults() #---reset plotting style
import matplotlib.font_manager
matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
fsize = 20
matplotlib.rcParams.update(
    {'font.size': fsize, 'xtick.major.size': 10, 'ytick.major.size': 10, 
     'xtick.major.width': 1, 'ytick.major.width': 1, 'ytick.minor.size': 5, 
     'xtick.minor.size': 5, 'xtick.direction': 'in', 'ytick.direction': 'in', 
     'axes.linewidth': 1, 'text.usetex': True, 'font.family': 'serif',
     'xtick.minor.size': 5, 'ytick.minor.size': 5, 'xtick.major.width': 1.5, 
     'ytick.major.width': 1.5, 'xtick.major.size': 10, 'ytick.major.size': 10,
     'xtick.major.pad': '8', 'ytick.major.pad': '8',
     #'legend.numpoints': 1, 'legend.columnspacing': 1,
     'legend.fontsize': fsize-4, 'xtick.top': True, 'ytick.right': True,
     'axes.grid': False, 'grid.color': 'lightgrey', 'grid.linestyle': ':', 
     'grid.linewidth': 3})


def read_in_account(account):
    
    df_faccount = pd.read_csv(account)

    return df_faccount

def read_in_transactions(trasaction):
    
    df_ftxn = pd.read_csv(transaction)

    return df_ftxn


def merge_datasets():
    
    df_merged = pd.merge(read_in_account(account), 
                         read_in_transactions(transaction), 
                         left_on='ACCTID', right_on='TOACCTID')

    return df_merged


def transaction_onto_self(df_transactions):
    
    self_transactions = df_transactions[ df_transactions['FROMACCTID'] == 
                                        df_transactions['TOACCTID'] ]
    
    return self_transactions




def hist_transactions(data, nbins, lin_log):
    
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.hist(data,  bins = np.linspace(min(data), max(data), nbins), 
            color='lightgrey', edgecolor='k', label='Self transactions')


    ax.set_ylabel(r"Number of transactions")
    ax.set_xlabel(r"Amount transferred")

    ax.set_yscale(lin_log)


    plt.legend(loc=0)
    plt.show()


def hist_specific_account(df_transactions, account_number, bins):
    
    axx = df_transactions['AMOUNT'] [df_transactions['FROMACCTID'] 
                                     == account_number]

    # Get gausian 
    kde = stats.gaussian_kde(axx)
    
    xx = np.linspace(0, max(axx), 100)
    
    fig, ax = plt.subplots(figsize=(7,7))
    ax.hist(axx, density=True, bins=bins, alpha=0.3, color='grey')
    ax.plot(xx, kde(xx))

    ax.set_ylabel(r"Density")
    ax.set_xlabel(r"Amount transferred")

    plt.show()

def hist_many_account(df_transactions, begin, end, bins):
    """
    There are several ranges where most transactions happen, narrow them by
    placing begin/end value of the transaction amount
    0 - 5000
    5000 - 10000
    Around 100 000
    Around 200 000
    
    Parameters
    ----------
    df_transactions : Dataframe
    begin : number
    end : number
    bins : number of beans

    Returns
    -------
    Plot

    """
    
    xx = np.linspace(begin, end, 1000)
    unique_from_acct = np.unique(df_transactions['FROMACCTID'])

    # Take X colors from a colormap
    #colors = cmr.take_cmap_colors('cmr.lilac', len(unique_from_acct), 
    #                              cmap_range=(0, 1), return_fmt='hex')

    fig, ax = plt.subplots(figsize=(7,7))
    
    
    all_kde = []
    for i, acc in enumerate(unique_from_acct):
    
        try:
            axx = df_transactions['AMOUNT'][df_transactions['FROMACCTID'] == 
                                            acc]
        
            kde = stats.gaussian_kde(axx)
            all_kde.append(kde)
            
        # Few accounts have only a several transactions    
        except np.linalg.LinAlgError:
            pass
        
        ax.plot(xx, kde(xx), color='lightgrey')#colors[i])
        
    plt.show()




if __name__ == "__main__":
    
    # Load in files
    account = '../../Hack_Defence/data/faccount.txt'
    transaction = '../../Hack_Defence/data/ftxn2.txt'

    # Read in data etc.
    df_accounts = read_in_account(account)
    
    df_transactions = read_in_transactions(transaction)
    
    df_merged = merge_datasets()
    
    self_transactions = transaction_onto_self(df_transactions)
    
    # Self transactions
    hist_transactions(self_transactions['AMOUNT'], 20, 'linear')
    # All transactions, log scale
    hist_transactions(df_transactions['AMOUNT'], 200, 'log')
    # Distribution of all transaction
    hist_specific_account(df_transactions, 500000, 50)
    
    # Distribution of all transactions, split into Amount range
    hist_many_account(df_transactions, 0, 4000, 50)
    hist_many_account(df_transactions, 4000, 10000, 50)
    hist_many_account(df_transactions, 90000, 105000, 50)
    hist_many_account(df_transactions, 199900, 200100, 50)
    
