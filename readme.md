# 接口说明
# copyright@gavinc

host：47.105.74.100:5000
所有请求方法均为POST

## 挂单指令
url：/send_order
传入参数示例：
{'direction':'open', 'localid': '123456', 'long_price': 2.3, 'long_amount': 1, 'short_price': 2.259, 'short_amount': 1}
说明：
参数名              类型        备注
direction       string      open：开仓，close：平仓
localid         string      本地使用的ID
long_price      float       多单价格
long_amount     float       多单数量（张）
short_price     float       空单价格
short_amount    float       空单数量（张）
返回结果示例：
 {"buy_price":"2.259","sell_price":"2.3","status":true}

## 撤单
url：/cancel_order
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
返回结果示例： 
{"status":true}

## 查单
url：/check_order
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
返回结果示例： 
{
    "buy_order":{
        "amount":null,
        "filled_amount":4,
        "filled_price":2,
        "order_id":"13213246546",
        "price":null
        },
    "sell_order":{
        "amount":null,
        "filled_amount":6,
        "filled_price":2,
        "order_id":"13213246546",
        "price":null
        },
    "status":true
}

## 查看收益
url：/check_profit 
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
{"order_id":"123456","profit":0.0,"status":true}

## 挂单转市单
url：/maker2taker 
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
{"status":true}

## 修单
url：/fix_order 
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
{"status":true}

## 修改市场单
url：/fix_market_order 
传入参数示例：
{'localid': '123456'}   //localid必须是用send_order接口下过单的
{"status":true}

