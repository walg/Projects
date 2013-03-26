#Foster Bettman 94722299
import indicators
class moving_average_signal:
    
    #class takes in the list of prices 
    def __init__(self,list_of_prices,list_of_moving_averages):
        self._list_of_prices = list_of_prices
        self._list_of_moving_averages = list_of_moving_averages


    #retrives individual item from eitherlist            
    def get_one_price(self, index):
        return self._list_of_prices[index]
    def get_one_moving_average(self, index):
        return self._list_of_moving_averages[index]

    #this will be the function called; returns None, Sell or Buy
    def assess_one_price(self,index):

        #compares each price to its moving average
        #returns SELL if moving_average is less than current price
        #returns BUY if moving_average is greater than current price
        #returns None otherwise
    
        closing_price = self.get_one_price(index)
        moving_average = self.get_one_moving_average(index)

        #if the moving average is empty (due to insufficient days to calculate it)
        #return empty string (means no signal, will not print anything in final report)
        if moving_average == '':
            return ''
        if closing_price < moving_average: #price is less than moving average - SELL
            return 'SELL'
        elif closing_price > moving_average: #price is more than moving average - BUY
            return 'BUY'
        else: #price stays the same
            return ''

    def execute(self):
        '''assess all prices in a list'''
        comparison_list = []
        last_assessment = None
        for x in range(len(self._list_of_prices)):
            #assessment is either BUY, SELL or None
            assessment = self.assess_one_price(x)
            if assessment == last_assessment:
                #eliminates redundancy by returning empty string for consecutive
                #BUYS or SELLS
                comparison_list.append('')
                continue
            comparison_list.append(assessment)
            last_assessment = assessment
        return comparison_list
    

class directional_signal:

    def __init__(self,list_of_prices,list_of_indicators,positive_threshold,negative_threshold):
        self._list_of_prices = list_of_prices
        self._list_of_indicators = list_of_indicators
        self._positive_threshold = positive_threshold
        self._negative_threshold = negative_threshold

    def get_one_price(self, index):
        return self._list_of_prices[index]
    def get_one_indicator(self, index):
        return self._list_of_indicators[index]
    def get_positive_threshold(self):
        return self._positive_threshold
    def get_negative_threshold(self):
        return self._negative_threshold
    
    def assess_one_price(self,index):

        #compares each price to its moving average
        #returns SELL if indicator is less than negative_threshold
        #returns BUY if indicator is greater than positive_threshold
        #returns '' otherwise
    
        closing_price = self.get_one_price(index)
        indicator = self.get_one_indicator(index)

        #if the moving average is None (due to insufficient days to calculate it
        #return empty string (means no signal, will not print anything in final report)
        if indicator > self._positive_threshold: # BUY
            result = 'BUY'
        elif indicator < self._negative_threshold: # SELL
            result = 'SELL'
        else:
            result = ''
        return result
    
    def execute(self):
        '''assess all prices in a list'''
        comparison_list = []
        last_assessment = None
        for x in range(len(self._list_of_prices)):
            #assessment is either BUY, SELL or None
            
            assessment = self.assess_one_price(x)
            if comparison_list == [] or assessment == last_assessment:
                #eliminates redundancy by returning empty string for consecutive
                #BUYS or SELLS
                comparison_list.append('')
                continue
            comparison_list.append(assessment)
            last_assessment = assessment
        return comparison_list
