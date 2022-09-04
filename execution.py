#region imports
from AlgorithmImports import *
#endregion


class Execution():
    """
    This class enssentially is to scan the portfolio again and sell those 
    """
    def __init__(self, liq_tol):
        self.liq_tol = liq_tol
    
    
    def ExecutePortfolio(self, algorithm, portfolio):
        """
        This is the main function in this class
        """
        # whether sell or hold certain stocks in terms of the liquidity tolerance
        liquidate_securities = portfolio[abs(portfolio) < self.liq_tol].index 
        holding_port = portfolio[abs(portfolio) >= self.liq_tol]
        
        self.LiquidateSecurities(algorithm, liquidate_securities)
        self.SetPortfolioHoldings(algorithm, holding_port)
    
    
    def LiquidateSecurities(self, algorithm, securities):
        """
        Helper function for ExecutePortfolio() to sell stocks below liquidity tolerance benchmark
        """
        liquid_count = 0
        for security in securities:
            if algorithm.Securities[security].Invested:
                algorithm.Liquidate(security)
                liquid_count += 1

    
    def SetPortfolioHoldings(self, algorithm, portfolio):
        for security, weight in portfolio.iteritems():
            algorithm.SetHoldings(security, weight)