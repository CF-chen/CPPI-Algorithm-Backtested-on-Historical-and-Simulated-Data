#region imports
from AlgorithmImports import *
#endregion
class FactorUniverseSelectionModel():
    def __init__(self, algorithm):
        self.algorithm = algorithm
    
    def SelectCoarse(self, coarse):
        """
        Main functin 1: get all tickers of stocks whose price is larger than 1 dollar and which are at the top 1000 by volumes
        """
        # self.algorithm.Log("Generating universe...")
        universe = self.FilterDollarPriceVolume(coarse)
        return [c.Symbol for c in universe]

    def SelectFine(self, fine):
        """
        Main function 2: get top 50 and bottom 50 tickers of stocks by CashReturn, excluded finanical stocks
        """
        universe = self.FilterFactor(self.FilterFinancials(fine))
        # self.algorithm.Log(f"Universe consists of {len(universe)} securities")
        self.algorithm.securities = universe
        return [f.Symbol for f in universe]
    
    def FilterDollarPriceVolume(self, coarse):
        """
        Helper function for SelectCoarse():
            To filter out stocks which have price less than 1 dollar 
            and sort all the stocks by their volumes and only keep top 1000 stocks
        """
        filter_dollar_price = [c for c in coarse if c.Price > 1]
        sorted_dollar_volume = sorted([c for c in filter_dollar_price if c.HasFundamentalData], key=lambda c: c.DollarVolume, reverse=True)
        return sorted_dollar_volume[:1000]

    def FilterFinancials(self, fine):
        """
        Helper function for SelectFine():
        Get rid of financial stocks
        """
        filter_financials = [f for f in fine if f.AssetClassification.MorningstarSectorCode != MorningstarSectorCode.FinancialServices]
        return filter_financials
    
    def FilterFactor(self, fine):
        """
        Helper function for SelectFine():
        sort fine data by CashReturn, get only top 50 and bottom 50 stocks
        """
        filter_factor = sorted(fine, key=lambda f: f.ValuationRatios.CashReturn, reverse=True)
        return filter_factor[:50] + filter_factor[-50:]