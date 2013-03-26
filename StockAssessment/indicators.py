#Foster Bettman 94722299
class simple_moving_average:
    def __init__(self, number, list_of_prices):
        self._number = number
        self._list_of_prices = list_of_prices
    def find_one_average(self,index):
        total = 0
        for x in range(index - self._number +1 , index+1):
            #loops through, totalling up the prices from the last N days and
            #divides by N
            if x < 0:
                #if there are too few days to calculate running average, immediately
                #stop function and return the average as empty string
                return ''
            total += self._list_of_prices[x]
        return total/self._number

    def execute(self):
        moving_average_list = []
        todays_average = 0
        for x in range(len(self._list_of_prices)):
            todays_average = self.find_one_average(x)
            moving_average_list.append(todays_average)
        return moving_average_list

class directional_indicator:
    def __init__(self, number, list_of_prices):
        self._number = number
        self._list_of_prices = list_of_prices

    def find_one_indicator(self,index):
        positive_counter = 0
        negative_counter = 0
        previous = 0
        current = 0
        for x in range(index - self._number, index + 1):

            #Loops through N days previous to the day given as index
            #up to index + 1, which includes the current day's indicator
        
            
            if x < 0 or x > len(self._list_of_prices):
                #does not count indices less than zero (list[-1] is the end of list etc.)
                #also does not count the instance where list index would be out
                #of range due to the (index + 1) in the for loop
                continue
            
            previous, current = current, self._list_of_prices[x]
            
            #previous is = to the current found in the last iteration
            #current is = to what is immediately read in
            
            if current > previous: #Stock went up
                positive_counter += 1
            elif current < previous: #Stock went down
                negative_counter -= 1
            else: #Stock stayed the same
                continue
            
        positive_counter -= 1   #Deals with the fact that initializing previous
                                #to zero automatically makes the first day's price
                                #register as the price going up, when it should be no change
        return positive_counter + negative_counter
    def execute(self):
        '''finds list of directional indicators given prices'''
        list_of_indicators = []
        positive_counter = 0
        negative_counter = 0
        previous = 0
        current = 0
        for x in range(len(self._list_of_prices)):
            todays_indicator = self.find_one_indicator(x)
            list_of_indicators.append(todays_indicator)
        
        return list_of_indicators
        
