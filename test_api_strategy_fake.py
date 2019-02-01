import requests, json, sys, unittest
sys.path.append('../')

# host = '47.105.74.100:5000'
host = '127.0.0.1:5000'
localid = '123456'

send_order_content = {'localid': localid, 'short_price': 2.3, 'short_amount': 1, 'long_price': 2.259, 'long_amount': 1}
url = 'http://'+host+'/send_order'
send_order_res = requests.post(url, data=send_order_content)
print(send_order_res.url, send_order_res.text)

check_order_content = {'localid': localid}
url = 'http://'+host+'/check_order'
check_order_res = requests.post(url, data=check_order_content)
print(check_order_res.url, check_order_res.text)

check_profit_content = {'localid': localid}
url = 'http://'+host+'/check_profit'
check_profit_res = requests.post(url, data=check_profit_content)
print(check_profit_res.url, check_profit_res.text)

maker2taker_content = {'localid': localid}
url = 'http://'+host+'/maker2taker'
maker2taker_res = requests.post(url, data=maker2taker_content)
print(maker2taker_res.url, maker2taker_res.text)

fix_order_content = {'localid': localid}
url = 'http://'+host+'/fix_order'
fix_order_res = requests.post(url, data=fix_order_content)
print(fix_order_res.url, fix_order_res.text)

fix_market_order_content = {'localid': localid}
url = 'http://'+host+'/fix_market_order'
fix_market_order_res = requests.post(url, data=fix_market_order_content)
print(fix_market_order_res.url, fix_market_order_res.text)

cancel_order_content = {'localid': localid, 'action': 'cancel_order'}
url = 'http://'+host+'/cancel_order'
cancel_order_res = requests.post(url, data=cancel_order_content)
print(cancel_order_res.url, cancel_order_res.text)