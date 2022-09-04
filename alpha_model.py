#region imports
from AlgorithmImports import *
#endregion
import pandas as pd

def normalise(series, equal_ls=True):
    """
    it's just a function to normalise a series of numbers
    """
    if equal_ls:
        series -= series.mean()
    sum = series.abs().sum()
    return series.apply(lambda x: x/sum)
    

class ValueAlphaModel():
    """
    To get alpha score by calculating the weights of cash return for each candidate stock
    """
    def __init__(self):
        pass
    
    
    def GenerateAlphaScores(self, algorithm, securities):
        # algorithm.Log(f"Generating alpha scores for {len(securities)} securities...")
        
        fcf_y = pd.DataFrame.from_records(
            [
                {
                    'symbol': str(security.Symbol),
                    'fcf_y': security.ValuationRatios.CashReturn
                } for security in securities
            ]).set_index('symbol')
        fcf_y['alpha_score'] = normalise(fcf_y['fcf_y'], True)
        return fcf_y