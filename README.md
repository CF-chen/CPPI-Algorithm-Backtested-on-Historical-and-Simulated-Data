# Automated Trading System

This porject is based on QuantConnect which is an algorithmic trading platform who provides various ready-to-go libraries/modules. Some of the libraries/modules were inherited in this project.

The project is a python-based and objective-oriented programming which executes stocks selection and portfolio optimisation; rebalanced the portfolio at 1 PM everyday. Backtested the algorithem with historical data.

  - Stock selection: filtered high liquid US stocks first and then selected top and bottom 50 ones based on cash return for long/short strategy. 
  - Portfolio optimisation: optimised the portfolio by setting portfolio minimum turnover (to save from transaction fees), positions minimum weights (to avoid overweighted for certain stock) and positions minimum liquidity (to avoid certain stocks in the portfolio taking tiny amount of stakes).
  - Backtest: summarised key PnL metrics and visualised portfolio performance eg. exposure, concentration, etc.
