Hedge fund 5300 class project  
GTAA strategy  

Required packages:
Numpy
Scipy
argparse
datetime
matplotlib
pandas (See: https://pandas.pydata.org/)
pypfopt (See: https://pyportfolioopt.readthedocs.io/en/latest/)

main.py: main file to start everything
Strategy.py: core part of the strategy
mo.py: Momentum signal generation
ef.py: refinement1, weighting by Modern Portfolio Theory
plot.py: Plotting tools
data_cleaning.py: Not useful for user's
Data.csv: Cleaned Data

Please directly run main().py in terminal
Configuration:
    Basic:          python3 data.csv
    1st Refinement: python3 data.csv --weight=ef
    2nd Refinement: python3 data.csv --diversify 

