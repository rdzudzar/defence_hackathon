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



if __name__ == "__main__":
    
    account = '../../Hack_Defence/data/faccount.txt'
    transaction = '../../Hack_Defence/data/ftxn2.txt'

    df_accounts = read_in_account(account)
    
    df_transactions = read_in_transactions(transaction)
    
    df_merged = merge_datasets()