#https://www.coingecko.com/en/api
import requests

#Request a CoinGecko API url, unpack JSON into dict and return
def request_url(url):
    request_json = requests.get(url)
    request_dict = request_json.json()
    return request_dict

#Returns dict
#Customizable coingecko_markets_api call
def ping_api():
    url = 'https://api.coingecko.com/api/v3/ping'
    data = request_url(url)
    return data


#Returns dict
#Retrieve global market stats
def global_api():
    url = 'https://api.coingecko.com/api/v3/global'
    data = request_url(url)
    return data

def global_defi_api():
    url = 'https://api.coingecko.com/api/v3/global/decentralized_finance_defi'
    data = request_url(url)
    return data


#Returns list
#Customizable coingecko_markets_api call
def coins_list_api(include_platform='false'):
    url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=' + include_platform
    data = request_url(url)
    return data

#Returns list
#Customizable coins/markets API call
def coins_markets_api(vs_currency, category='', order='market_cap_desc', per_page='250', page='1', sparkline='false', price_change_percentage='24h'):
    #category = 'decentralized_finance_defi'
    price_change_percentage = '1h%2C24h%2C7d%2C30d%2C1y'

    url = ('https://api.coingecko.com/api/v3/coins/markets?vs_currency=' + vs_currency +
          '&category=' + category +
          '&order=' + order +
          '&per_page=' + per_page +
          '&page=' + page +
          '&sparkline=' + sparkline +
          '&price_change_percentage=' + price_change_percentage)

    data = request_url(url)
    return data

#Returns dict
#Customizable coins/{id} API call
def coins_id_api(id, localization='true', tickers='true', market_data='true', community_data='true', developer_data='true', sparkline='true'):
    url = ('https://api.coingecko.com/api/v3/coins/' + id +
          '?localization=' + localization +
          '&tickers=' + tickers +
          '&market_data=' + market_data +
          '&community_data=' + community_data +
          '&developer_data=' + developer_data +
          '&sparkline=' + sparkline)

    data = request_url(url)
    return data

#Returns dict
#Customizable coins/{id}/history API call
def coins_id_history_api(id, date, localization='true'):
    url = ('https://api.coingecko.com/api/v3/coins/' + id +
          '/history?date=' + date +
          '&localization=' + localization)

    data = request_url(url)
    return data

#Returns dict
#Customizable coins/{id}/market_chart API call
def coins_id_market_chart_api(id, vs_currency, days='1', interval='hourly'):
    url = ('https://api.coingecko.com/api/v3/coins/' + id +
          '/market_chart?vs_currency=' + vs_currency +
          '&days=' + days +
          '&interval=' + interval)

    data = request_url(url)
    return data

#Returns dict
#Customizable coins/{id}/market_chart/range API call
def coins_id_market_chart_range_api(id, vs_currency, from_unix, to_unix):
    url = ('https://api.coingecko.com/api/v3/coins/' + id +
          '/market_chart/range?vs_currency=' + vs_currency +
          '&from=' + from_unix +
          '&to=' + to_unix)

    data = request_url(url)
    return data



#Returns list
def exchanges_api(per_page='100', page='1'):
    url = ('https://api.coingecko.com/api/v3/exchanges?per_page=' + per_page +
           '&page=' + page)

    data = request_url(url)
    return data

#Returns dict
def exchanges_id_api(id):
    url = 'https://api.coingecko.com/api/v3/exchanges/' + id
    data = request_url(url)
    return data

#Returns list of lists(unix time, volume)
def exchanges_id_volume_chart_api(id, days='1'):
    url = ('https://api.coingecko.com/api/v3/exchanges/' + id +
           '/volume_chart?days=' + days)

    data = request_url(url)
    return data


#Returns dict
#Return BTC to fiat exchange rates
def exchange_rates_api():
    url = 'https://api.coingecko.com/api/v3/exchange_rates'
    data = request_url(url)
    return data

#Returns dict
#Retrieve Top 7 trending coins on CoinGecko
def search_trending_api():
    url = 'https://api.coingecko.com/api/v3/search/trending'
    data = request_url(url)
    return data



#Contracts
#Finance
#Indexes
#Derivatives
#Status Updates
#Events