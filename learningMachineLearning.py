import pandas as pd
import Quandl 

df = Quandl.get('WIKI/GOOGL')

df = df[['Adj. Open','Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
