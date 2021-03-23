import requests




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


def display_exchange_info(exchange_info):
    print(exchange_info.get('name'))
    print('Trust Score: ' + str(exchange_info.get('trust_score')))
    print('24-Hour BTC Volume: ' + "{:.2f}".format(exchange_info.get('trade_volume_24h_btc')) + ' BTC')
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







#Waiting period

def main():
    # Define exchange to operate on from exchanges_api id
    exchanges = ['gdax', 'binance_us', 'bittrex']
    blacklist = ['USDT', 'BUSD', 'USDC', 'WBTC', 'DAI', 'UST', 'BCH', 'CUSD']

    vs_currency = 'BTC'
    exchange_id = exchanges[2]
    base_currencies, target_currencies = get_exchange_tickers(exchange_id)


    exchange_info = exchanges_id_api(exchange_id)
    display_exchange_info(exchange_info)



    #Print base and target currencies for current exchange
    print('Base Currencies available on: ' + exchange_info.get('name'))
    print(base_currencies)
    print('Target Currencies available on: ' + exchange_info.get('name'))
    print(target_currencies)

    #display_data(exchanges_api('25'))


if __name__ == '__main__':
    main()






#Compile list of error codes