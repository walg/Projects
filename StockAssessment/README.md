This is the 3rd of 5 projects in ICS 32 during winter quarter.
The class is taught by Professor Alex Thornton and is located at the University of California, Irvine.

This program reads in the date and corresponding closing price of a particular stock from Yahoo. Then, based either on a 
simple moving average or directional indicators (number of days where the price closed higher than the day before minus
the number of days where price closed lower than the day before) tell the user "BUY" or "SELL."

The program is split into four modules: 
-'main' is the module that should be run. It contains functions that verify correct input and read in information from other
modules
-'indicators' contains the 2 types of indicators, each given its own class. They take a list of prices and return their
respective indicators
-'signal_strategies' take the list of indicators and returns a list of 'BUY', 'SELL' or None 
-'request_URL' takes in the stock's ticker symbol, start, and end dates to get information from Yahoo within that
time frame. 

How the indicators work:
-Simple Moving average: Given a number n, takes the average price counting n days back from the current day. Because it's
always n days back from the current day, not a set day, the simple moving average moves with the data. The strategy using
this is that if the simple moving average falls below the current price, the user is told to sell. The user is told
to buy when the simple moving average climbs above the current price.

-Directional Indicators: Given a number n, counts starting from n days back until the current day how many times the stock 
price closed above or below the next day's price. Finds the difference of the two. If the difference falls below a given 
threshold, the user is told to sell. If the difference climbs above another given threshold, the user is told to buy. 
