#region imports
from AlgorithmImports import *
#endregion
from universe_selection import FactorUniverseSelectionModel
from alpha_model import ValueAlphaModel
from portfolio_construction import OptimisationPortfolioConstructionModel
from execution import Execution
from charting import InitCharts, PlotPerformanceChart, PlotPosConcentrationChart, PlotStockCountChart, PlotExposureChart

class TradingBot(QCAlgorithm):
    def Initialize(self):
        # Setup time spam and cash
        self.SetStartDate(2021, 9, 1)
        self.SetCash(100000)
        
        # Data resolution
        self.UniverseSettings.Resolution = Resolution.Minute
        
        # Universe selection model: Universe selection is the process of selecting a basket of assets you may trade. 
        self.securities = []
        self.CustomUniverseSelectionModel = FactorUniverseSelectionModel(self) 
        self.AddUniverse(self.CustomUniverseSelectionModel.SelectCoarse, self.CustomUniverseSelectionModel.SelectFine) 
        
        # Alpha model: to identify specific stocks to trade
        self.CustomAlphaModel = ValueAlphaModel()
        
        # Portfolio construction model: set maximum weights for any element in a portfolio to be 5%, the min turnover to be 5%
        self.CustomPortfolioConstructionModel = OptimisationPortfolioConstructionModel(turnover=0.05, max_wt=0.05, longshort=True)
        
        # Execution model
        self.CustomExecution = Execution(liq_tol=0.005)
        
        # Add SPY for trading days data -- benchmark
        ticker = 'SPY'
        self.AddEquity(ticker, Resolution.Daily)
        
        # Schedule rebalancing: execute RebalancePortfolio function at 13.00 everyday
        self.Schedule.On(self.DateRules.EveryDay(ticker), self.TimeRules.At(13, 0), Action(self.RebalancePortfolio))
        
        # Initilise charting
        InitCharts(self)
        
        # Schedule charting
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Friday), self.TimeRules.BeforeMarketClose(ticker, 0), Action(self.PlotCharts))

        
    def OnData(self, data):
        """
        This function to input self defined data. I used data provided by QuantConnect in this project.
        """
        pass
    
    
    def RebalancePortfolio(self): 
        alpha_df = self.CustomAlphaModel.GenerateAlphaScores(self, self.securities) # get the alpha score
        portfolio = self.CustomPortfolioConstructionModel.GenerateOptimalPortfolio(self, alpha_df)  # generate a new portfolio based on alpha scores under two constraints turnover and max_weights
        self.CustomExecution.ExecutePortfolio(self, portfolio) # excute the new portfolio with liquidity tolerace = 0.005
    
    
    def PlotCharts(self):
        """
        A helper function to run the chartting algos
        """
        PlotPerformanceChart(self)
        PlotPosConcentrationChart(self)
        PlotStockCountChart(self)
        PlotExposureChart(self)