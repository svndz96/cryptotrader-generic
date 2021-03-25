import requests
from operator import itemgetter
from url_functions import *




#Define API keys to interact for selected exchange, come up with secure method, env variables or OAuth

#Compile list of vs_currencies and supported coins on platform

def exchanges_api(per_page='100', page='1'):
    url = ('https://api.coingecko.com/api/v3/exchanges?per_page=' + per_page + '&page=' + page)

    data = request_url(url)
    return data

def exchanges_id_api(id):
    url = 'https://api.coingecko.com/api/v3/exchanges/' + id
    data = request_url(url)
    return data

def display_data(data):
    for item in data:
        for key in item:
            print('{}: '.format(key) + str(item[key]))
        print('')

#Exchange connectivity code

def request_url(url):
    request_json = requests.get(url)
    request_dict = request_json.json()
    return request_dict


def display_exchange_info(exchange_info, rates):
    print(exchange_info.get('name'))
    print('Trust Score: ' + str(exchange_info.get('trust_score')))
    print('Bitcoin 24h Volume: ' + "{:.2f} BTC".format(exchange_info.get('trade_volume_24h_btc')))
    print('USD 24h Volume: ' + "${:,.2f}".format(exchange_info.get('trade_volume_24h_btc') * rates.get('usd').get('value')))
    print('URL: ' + str(exchange_info.get('url')))
    print()

def get_exchange_tickers(exchange):
    base_currencies = []
    target_currencies = []

    exchange_info = exchanges_id_api(exchange)
    tickers = exchange_info.get('tickers')
    for item in tickers:
        #print(item)
        base = item.get('base')
        target = item.get('target')

        if base not in base_currencies:
            base_currencies.append(base)
        if target not in target_currencies:
            target_currencies.append(target)

    return base_currencies, target_currencies


#Return BTC to fiat exchange rates
def exchange_rates_api():
    url = 'https://api.coingecko.com/api/v3/exchange_rates'
    data = request_url(url)
    return data


#Bot class - Waits until conditions are met to initiate trade,
# will standby waiting to sell and complete trade
# once certain profit is reached (recovered from dip, etc.)
class TradingBot:
    #standby - online and actively waiting for trading opportunity
    #trading - currently locked in a trade, waiting for exit and return to standby
    #intervention - waiting for user intervention on next action
    #offline - bot disconnected, maintenance, rebooting
    #error - unexpected error occurs, bugs
    current_status = ['standby', 'trading', 'intervention', 'offline', 'error']

    exchange = 'Coinbase'
    #API Keys to interact with exchange
    keys = {}
    #Target market to trade against
    reserve_asset = 'BTC'
    #All cryptos on current exchange
    crypto_list = []
    #Priority list to purchase first
    watchlist = []
    #Cryptos to completely avoid
    blacklist = []

    #Amount in reserve available to purchase
    purchasing_power = 0
    #Limit on how much a bot can purchase, null is no limit
    purchase_limit = 0


    #Price when purchased and current price, profit made
    purchase_price = 0
    date_purchased = ''

    current_price = 0
    current_profit = 0

    #Price to wait for to initiate sell
    sell_price = 0
    sell_price_percentage = 0

    #Price of last sale, profit, and date sold
    last_sale_price = 0
    last_sale_profit = 0
    last_sale_date = ''


    #Trading Bot Performance
    #Statistics to compare and measure up to different bot types
    #Total trades completed(buying and selling) and total profit made since beginning
    total_trades = 0
    total_profit = 0

    #Average time of being locked in trade, from all trades
    average_time_held = 0
    #Average profit made total_profit/total_trades
    average_profit = 0


    def initiate_buy(self):
        pass

    def initiate_sell(self):
        pass

    def trade_completed(self):
        pass

    def update_total_profit(self):
        pass

    def update_average_time_held(self):
        pass

    def update_average_profit(self):
        pass



#Customizable coins/markets API call
def coins_markets_api(vs_currency, category='', order='market_cap_desc', per_page='250', page='1', sparkline='false', price_change_percentage='24h'):
    #category = 'decentralized_finance_defi'
    price_change_percentage = '1h%2C24h%2C7d%2C14d%2C30d%2C200d%2C1y'

    url = ('https://api.coingecko.com/api/v3/coins/markets?vs_currency=' + vs_currency +
          '&category=' + category +
          '&order=' + order +
          '&per_page=' + per_page +
          '&page=' + page +
          '&sparkline=' + sparkline +
          '&price_change_percentage=' + price_change_percentage)

    data = request_url(url)
    return data

#Take in sub list of cryptos and filter out by values
def crypto_filter(cryptos, timeframe, price_filter):
    filtered_list = []
    #Iterate through list and remove null results to sort
    for item in cryptos:
        if price_filter < 0:
            if item.get(timeframe) < price_filter:
                filtered_list.append(item)
        else:
            if item.get(timeframe) > price_filter:
                filtered_list.append(item)
    return filtered_list

#Take in sub list of cryptos to sort and return
def crypto_sorter(cryptos, sort, reverse):
    sorted_cryptos = sorted(cryptos, key=itemgetter(sort), reverse=reverse)
    return sorted_cryptos


#Waiting period

def main():
    # Define exchange to operate on from exchanges_api id
    exchanges = ['gdax', 'binance_us', 'bittrex']
    exchange_id = exchanges[2]

    vs_currency = 'USD'
    cryptos = coins_markets_api(vs_currency.lower())

    stablecoins = ['USDT', 'USDC', 'BUSD', 'DAI', 'UST', 'PAX', 'HUSD', 'TUSD', 'SUSD', 'USDN', 'VAI', 'GUSD', 'FRAX', 'USDP', 'ESD','USDX', 'KRT', 'MUSD',]
    blacklist = ['WBTC', 'WETH', 'BCH',]
    watchlist = []

    btc_rates = exchange_rates_api().get('rates')
    btc_usd = btc_rates.get('usd').get('value')

    investment = 200



    #Loop for each exchange
    for id in exchanges:
        #Create base vs target lists from exchange api
        base_currencies, target_currencies = get_exchange_tickers(id)

        # Update base_currencies by removing blacklist
        cropped_list = []
        for crypto in base_currencies:
            if (crypto not in stablecoins) and (crypto not in blacklist) and (crypto not in vs_currency):
                cropped_list.append(crypto)
        base_currencies = cropped_list


        #Retrieve and display exchange info, volume, etc.
        exchange_info = exchanges_id_api(id)
        display_exchange_info(exchange_info, btc_rates)

        print('Currently trading with: ' + vs_currency)
        print('Investment amount: ' + "{:,.2f}".format(investment))
        print()

        print('Target Currencies available on: ' + exchange_info.get('name'))
        print(target_currencies)
        #Print base and target currencies for current exchange
        print('Base Currencies available on: ' + exchange_info.get('name'))
        #print(base_currencies)
        print()

        #Create new filtered and sorted crypto list, removing null values
        timeframes = ['1h', '24h', '7d', '14d', '30d']
        timeframe = timeframes[1]

        # Sort and filter out list by percentage filters
        price_sorter = 'price_change_percentage_' + timeframe + '_in_currency'
        #If price_filter is negative, will check for lower values (bigger dumps)
        #If price_filter is positive, will check for higher values (bigger pumps)
        price_filter = -5
        filtered_cryptos = crypto_filter(cryptos, price_sorter, price_filter)
        sort_method = 'market_cap_rank'
        sorted_cryptos = crypto_sorter(filtered_cryptos, sort_method, True)


        #Iterate filtered list and display price info
        for crypto in sorted_cryptos:
            symbol = crypto.get('symbol').upper()
            price = crypto.get('current_price')
            price_change = crypto.get(price_sorter)
            if symbol in base_currencies:
                print("{}. ".format(crypto.get('market_cap_rank')) + crypto.get('name') + " ({}) ".format(symbol))
                print('Market Cap: ' + "${:,.2f}".format(crypto.get('market_cap')))
                print('Current Price: ' + "${:.2f}, ".format(price) + timeframe + " {:.2f}%".format(price_change))
                #Find price before price change
                print('Price after correction:' + " ${:.2f}".format(price + (price*abs(price_change)/100)))
                print('Profit:' + " ${:.2f}".format(investment*abs(price_change)/100))


                print()



        input('Enter to continue...')
        print('\n')







    #display_data(exchanges_api('25'))      #Print top 25 exchanges


if __name__ == '__main__':
    main()






#Compile list of coins to trade for based on exchange
#Wait for certain dip to occur (sleep)
#Execute buy order, save info (price, date, etc.)
#Wait for opportunity to sale (profits made, etc.)
#Execute sell order, update bot performance


#Compile list of error codes