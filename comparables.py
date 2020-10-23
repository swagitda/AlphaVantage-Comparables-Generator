import pandas_datareader.data as web
import datetime
import requests
import time
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries

key = 'YOURKEY'
ts = TimeSeries(key=key, output_format='pandas')
# Company_Overview = fd.get_company_overview(symbol)
# there seems to be a bug in the python library itself for the above, hence the workaround below

API_URL = "https://www.alphavantage.co/query"

symbols = ['CHKP', 'CRWD', 'CSCO', 'CYBR', 'FEYE', 'FTNT', 'MIME', 'NET', 'NLOK', 'OKTA', 'PANW', 'PFPT', 'QLYS', 'RPD', 'SAIL', 'SPLK', 'SUMO', 'TENB', 'ZS']
for symbol in symbols:
	data = {
	    "function": "OVERVIEW",
	    "symbol": symbol,
	    "outputsize": "compact",
	    "datatype": "json",
	    "apikey": key,
	}
	
	Stonk_Today = ts.get_quote_endpoint(symbol)
	Stonk_Monthly = ts.get_monthly_adjusted(symbol)
	Stonk_Daily = ts.get_daily_adjusted(symbol)
	response = requests.get(API_URL, data)
	Company_Overview = response.json()

	market_cap_billions = round(int(Company_Overview['MarketCapitalization']) / 1000000000, 1)

	ev_to_revenue = round(float(Company_Overview['EVToRevenue']), 1)

	stonk_price_today = float(Stonk_Today[0]['05. price'])

	try:
		stonk_price_jan_1 = float(Stonk_Monthly[0]['1. open']['2020-01-31'][0])
		ytd_stonk_change_percent = '{:.1%}'.format(stonk_price_today / stonk_price_jan_1 - 1)
	except:
		stonk_price_ipo = (Stonk_Daily[0]['1. open'][-1])
		ytd_stonk_change_percent = '{:.1%}'.format(stonk_price_today / stonk_price_ipo - 1)

	print(symbol, "$" + str(market_cap_billions) + "bn", "|", str(ev_to_revenue) + "x", "|", ytd_stonk_change_percent)
	time.sleep(60)