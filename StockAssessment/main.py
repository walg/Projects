#Foster Bettman 94722299
import signal_strategies
import request_URL
import indicators
def main():
    '''main function'''
    #reads in list of stock dates, their corresponding prices and stock symbol
    dates,prices,symbol = _make_valid_request()

    #reads in signal strategy and the number of days back to assess
    signal_strategy = _get_signal_strategy()
    days = _get_number_of_days_back()

    #finds list of averages and list of strategies for simple moving average
    if signal_strategy == 'Simple Moving Average':
        data = indicators.simple_moving_average(days,prices).execute()
        strategies = signal_strategies.moving_average_signal(prices, data).execute()

        #prints header and report data for simple moving average
        report = _create_report_header(symbol, signal_strategy, days)
        report += format_report(signal_strategy,dates,prices,data,strategies)

                                       
    #finds list of directional indicators and strategies for directional indicators
    elif signal_strategy == 'Directional':
        positive_threshold = _get_valid_threshold('positive')
        negative_threshold = _get_valid_threshold('negative')
        data = indicators.directional_indicator(days,prices).execute()
        strategies = signal_strategies.directional_signal(prices, data,positive_threshold,negative_threshold).execute()      

        #prints header and report data for directional indicators
        report = _create_report_header(symbol,signal_strategy, days, positive_threshold,negative_threshold)
        report += format_report(signal_strategy,dates,prices,data,strategies)

    print(report)
    


def format_report(signal_strategy,list_of_dates, list_of_prices, list_of_data, list_of_signals):
    #default template with which to format actual data
    report_template = '{:11}{:9.2f}   {:2}          {}'

    #this template is used for when simple moving average exists. rounds to 2 decimal places
    moving_average_template = '{:11}{:9.2f}    {:2.2f}     {}'
    report = ''

    #formats data
    for x in (range(len(list_of_dates))):
        if signal_strategy == 'Simple Moving Average' and type(list_of_data[x]) == float:
            report += moving_average_template.format(list_of_dates[x],list_of_prices[x],list_of_data[x],list_of_signals[x]) + '\n'
        else:
            report += report_template.format(list_of_dates[x],list_of_prices[x],list_of_data[x],list_of_signals[x]) + '\n'
    return report

def _create_report_header(symbol, signal_strategy, days, positive_threshold = None,negative_threshold = None):
    '''creates header with format
    SYMBOL: 
    STRATEGY: DIRECTIONAL/SIMPLE MOVING AVERAGE, buy above x, sell below y (directional only)
    '''
    header = ''
    header+= 'SYMBOL: {}\n'.format(symbol)

    #creates strategy line for simple moving averages
    if signal_strategy == 'Simple Moving Average':
        header+= 'STRATEGY: ' + signal_strategy + ', {} days back\n'.format(days)

    #creates strategy line for directional indicators
    elif signal_strategy == 'Directional':
        header += 'STRATEGY: {}, {} days back, buy above {}, sell below {}\n'.format(signal_strategy,days,positive_threshold,negative_threshold)
    header += '\n'

    #creates header for actual data
    header += 'DATE          CLOSE    INDICATOR  SIGNAL\n'
    return header

def _get_signal_strategy():
    '''gets signal strategy until user inputs valid strategy'''
    while True:
        signal_strategy = int(input(
        '''What is the desired signal strategy?
           1 - Simple Moving Average
           2 - Directional\n'''))
        if signal_strategy == 1:
            return 'Simple Moving Average'
        elif signal_strategy == 2:
            return 'Directional'
        else:
            print('Please input a valid strategy.')
            continue

def _get_number_of_days_back():
    '''gets user input for days back until user inputs correct form(as an int)
    '''
    while True:
        try:
            days = int(input('How many days back would you like to assess?'))
            return days
        except:
            print('please write a valid int')
            continue

def _get_valid_threshold(type_of_threshold: 'positive or negative'):
    '''gets a valid threshold from user, either positive or negative
    '''
    while True:
        try:
            threshold = int(input('What is the {} threshold?'.format(type_of_threshold)))
            return threshold
        except:
            print('please write a valid int')
            continue

###REQUEST URL###
        
def _make_valid_request():
    '''checks if the url request is valid, returns request only after it is valid
    '''
    while True:
        try:
            dates,prices,symbol = read_stocks()
            return (dates,prices,symbol)
        except:
            print('try again')
            continue

def read_stocks():
    '''reads in all stock information from the request_URL module
    stocks are a list of each line for each day of trading
    '''
    #reads in relevant stock request information from user
    symbol = input('What is the ticker symbol?')
    start_date = input('What is the start date')
    end_date = input('What is the end date?')

    #makes request
    request = request_URL.request_URL(symbol,start_date,end_date)
    stocks = request.request()

    date_list = []
    closing_list = []
    
    # loops through the list:
    #   decodes from bytes to strings 
    #   splits each line by commas
    #   retrieves only the date and closing price (indices 0,4)
    for x in range(len(stocks)):
        item = stocks[x].decode(encoding = 'utf-8')
        item_list = item.split(',')
        date_list.append(item_list[0])
        closing_list.append(float(item_list[4]))

    #reverses the list to descending chronological order
    date_list = date_list[::-1]
    closing_list = closing_list[::-1]
    
    #returns a tuple containing both lists as well as the symbol
    return (date_list,closing_list, symbol)

if __name__ == '__main__':
    main()
