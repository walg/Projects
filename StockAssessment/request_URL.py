#Foster Bettman 94722299
import urllib.request

class InvalidFormat(Exception):
    pass
class request_URL:
    def __init__(self, symbol, start_date, end_date):
        self._symbol = symbol
        self._start_date = start_date
        self._end_date = end_date


    def separate_date(self, date):
        '''retrieves the individual YYYY-MM-DD from the start or end date'''
        #splits given date by dashes
        #returns a dictionary with:
        #   year = YYYY
        #   month = MM
        #   day = DD
        year,month,day = date.split('-')

        #because requesting the month requires values from 0-11 and not 1-12,
        #automatically lower the value by 1 to match human input
        month = int(month)
        month -= 1
    
        full_date = dict(year = year, month = month, day = day)
        return full_date
    
    def separate_start_date(self):
        return self.separate_date(self._start_date)
    def separate_end_date(self):
        return self.separate_date(self._end_date)

    def request(self):
        '''attempts to request URL with format:
        http://ichart.yahoo.com/table.csv?s=SYMBOL&a=START_MONTH&b=START_DAY&c=START_YEAR&d=END_MONTH&e=END_DAY&f=END_YEAR&g=d
        '''
        #reads in both start and end dates
        start = self.separate_start_date()
        end = self.separate_end_date()

        #formats URL to put in given year/month/day for both start and end dates
        request_constructor = 'http://ichart.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d'.format(self._symbol,start['month'],start['day'],start['year'],
                                                                                                         end['month'],end['day'],end['year'])
        #requests and reads in the stock quotes
        #stock format is as follows:
        #   Date,Open,High,Low,Close,Volume,Adj Close
        #   each value separated by commas
        response = urllib.request.urlopen(request_constructor)
        stock_quotes = response.readlines()
        #removes header line
        stock_quotes.pop(0)

        #adds stock_quotes as a class variable for use if needed
        self._stock_quotes = stock_quotes
        
        #returns each line as a list. Returns all values in case others are needed
        #even though only dates and closes are needed right now
        return stock_quotes
