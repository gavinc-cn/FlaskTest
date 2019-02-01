from circuits import Event
from decimal import Decimal
from base import base_utils
from base.logconf import logger


class Depth(Event):
    def __init__(self, exchange_key, market, symbol, source, asks, bids, servertime, localtime, raw=None):
        super().__init__(exchange_key, market, symbol, source, asks, bids, servertime, localtime, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.asks = asks
        self.bids = bids
        self.servertime = servertime
        self.localtime = localtime
        self.raw = raw

    def slip(self, side, target_amount):
        """
        :param side:
        :param target_amount: amount 为合约张数
        :return:
        """
        res = self

        total_amount = Decimal(0)
        total_price = Decimal(0)
        side_list = res.bids if side == 'buy' else res.asks
        for i in side_list:
            if total_amount + Decimal(i[1]) >= target_amount:
                total_price += Decimal(i[0]) * (target_amount - total_amount)
                total_amount = target_amount
                break
            total_amount += Decimal(i[1])
            total_price += Decimal(i[0]) * Decimal(i[1])
        return total_price / total_amount


class Ticker(Event):
    def __init__(self, exchange_key, market, symbol, source, servertime, localtime, lastprice, high24, low24, sell, buy, vol24, raw=None):
        super().__init__(exchange_key, market, symbol, source, servertime, localtime, lastprice, high24, low24, sell, buy, vol24, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.lastprice = lastprice
        self.high24 = high24
        self.low24 = low24
        self.sell = sell
        self.buy = buy
        self.vol24 = vol24
        self.raw = raw
        # print('EVENT_TICKER:', lastprice)


class Kline(Event):
    def __init__(self, exchange_key, market, symbol, source, servertime, localtime, open, high, low, close, volume, raw):
        super().__init__(exchange_key, market, symbol, source, servertime, localtime, open, high, low, close, volume, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.raw = raw


class Deals(Event):
    def __init__(self, exchange_key, market, symbol, source, servertime, localtime, trade_id, price, size, side, raw):
        super().__init__(exchange_key, market, symbol, source, servertime, localtime, trade_id, price, size, side, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.trade_id = trade_id
        self.price = price
        self.size_piece = size
        self.side = side
        self.raw = raw


class SpotAccount(Event):
    def __init__(self, exchange_key,market, coin, servertime, localtime, free, freezed, raw):
        super().__init__(exchange_key,market, coin, servertime, localtime, free, freezed, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.coin = coin
        self.servertime = servertime
        self.localtime = localtime
        self.free = free
        self.freezed = freezed
        self.raw = raw


class MarginAccount(Event):
    def __init__(self, exchange_key, market, symbol, coin, servertime, localtime, free, freezed, borrowed, lending_fee, raw):
        super().__init__(exchange_key, market, symbol, coin, servertime, localtime, free, freezed, borrowed, lending_fee, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.coin = coin
        self.servertime = servertime
        self.localtime = localtime
        self.free = free
        self.freezed = freezed
        self.borrowed = borrowed
        self.lending_fee = lending_fee
        self.raw = raw


class FutureAccount(Event):
    def __init__(self, exchange_key, market, coin, servertime, localtime, balance, keep_deposit, profit_real, raw):
        super().__init__(exchange_key, market, coin, servertime, localtime, balance, keep_deposit, profit_real, raw)
        self.exchange_key = exchange_key    # 交易对唯一标识
        self.market = market                # 交易所
        self.coin = coin                    # 币种
        self.servertime = servertime        # 服务器时间
        self.localtime = localtime          # 客户端时间
        self.balance = balance              # 账户余额
        self.keep_deposit = keep_deposit    # 保证金
        self.profit_real = profit_real      # 已实现盈亏
        self.raw = raw                      # 原始数据


class ForecastPrice(Event):
    def __init__(self, exchange_key, market, coin, source, servertime, localtime, price, raw):
        super().__init__(exchange_key, market, coin, source, servertime, localtime, price, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.coin = coin
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.price = price
        self.raw = raw


class FutureIndex(Event):
    def __init__(self, exchange_key, market, coin, source, servertime, localtime, price, raw):
        super().__init__(exchange_key, market, coin, source, servertime, localtime, price, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.coin = coin
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.price = price
        self.raw = raw


class Position(Event):
    def __init__(self, exchange_key, market, servertime, localtime, coin, symbol, long_avgprice, short_avgprice, long_eveningup, short_eveningup, long_hold_amount, short_hold_amount, realized, raw):
        super().__init__(exchange_key, market, servertime, localtime, coin, symbol, long_avgprice, short_avgprice, long_eveningup, short_eveningup, long_hold_amount, short_hold_amount, realized, raw)
        self.exchange_key = exchange_key            # 交易对唯一标识
        self.market = market                        # 交易所
        self.servertime = servertime                # 服务器时间
        self.localtime = localtime                  # 本地时间
        self.coin = coin                            # 币种
        self.symbol = symbol                        # 交易对
        self.long_avgprice = long_avgprice          # 多仓平均价
        self.short_avgprice = short_avgprice        # 空仓平均价
        self.long_eveningup = long_eveningup        # 多仓可平仓数量
        self.short_eveningup = short_eveningup      # 空仓可平仓数量
        self.long_hold_amount = long_hold_amount    # 多仓持仓量
        self.short_hold_amount = short_hold_amount  # 空仓持仓量
        self.realized = realized                    # 已实现盈亏
        self.raw = raw                              # 原始返回数据


class FundingRate(Event):
    def __init__(self, exchange_key, market, symbol, source, servertime, localtime, funding_rate, interest_rate, raw):
        super().__init__(exchange_key, market, symbol, source, servertime, localtime, funding_rate, interest_rate, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.funding_rate = funding_rate
        self.interest_rate = interest_rate
        self.raw = raw


class PriceRange(Event):
    def __init__(self, exchange_key, market, symbol, source, servertime, localtime, highest, lowest, raw):
        super().__init__(exchange_key, market, symbol, source, servertime, localtime, highest, lowest, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.source = source
        self.servertime = servertime
        self.localtime = localtime
        self.highest = highest
        self.lowest = lowest
        self.raw = raw


class OrderFeedback(Event):
    def __init__(self, exchange_key=None, market=None, symbol=None, order_id=None, localid=None, servertime=None, localtime=None, source=None, status=None, policy=None, method=None, price=None, filled_price=None, amount=None, filled_amount=None, side=None, raw=None):
        super().__init__(exchange_key, market, symbol, order_id, localid, servertime, localtime, source, status, policy, method, price, filled_price, amount, filled_amount, side, raw)
        self.exchange_key = exchange_key
        self.market = market
        self.symbol = symbol
        self.order_id = order_id
        self.localid = localid
        self.servertime = servertime
        self.localtime = localtime
        self.source = source
        self.status = status
        self.policy = policy
        self.method = method
        self.price = price
        self.filled_price = filled_price
        self.amount = amount
        self.filled_amount = filled_amount
        self.side = side
        self.raw = raw
        # print('OrderFeedback Event:',self.localid, self.status)


class Order(Event):
    def __init__(self, exchange_key, market, symbol, order_id, localid, servertime, localtime, source, status, policy=None, method=None, price=None, filled_price=None, amount=None, filled_amount=None, side=None, raw=None):
        super().__init__(exchange_key, market, symbol, order_id, localid, servertime, localtime, source, status, policy, method, price, filled_price, amount, filled_amount, side, raw)
        self.exchange_key = exchange_key    # Rest Scock 都有
        self.market = market                # Rest Sock 都有
        self.symbol = symbol                # Rest Sock 都有
        self.order_id = order_id            # Rest Sock 都有
        self.localid = localid              # 只有Rest有
        self.servertime = servertime        # Rest Sock 都有，以legal的更新为准
        self.localtime = localtime          # Rest Sock 都有，以legal的更新为准
        self.source = source                # Rest Sock 都有，以legal的更新为准
        self.status = status                # Rest Sock 都有，以legal的更新为准
        self.policy = policy                # 只有Rest有
        self.method = method                # 只有Rest有
        self.price = price                  # Rest Sock 都有，Sock可能会更新，以Sock为准
        self.filled_price = filled_price
        self.amount = amount                # Rest Sock 都有，Sock可能会更新，以Sock为准
        self.filled_amount = filled_amount  # Rest初始为0，后续会通过Sock更新
        self.side = side                    # 只有Rest有, 必须update_weak
        self.raw = raw
        # print('ORDER_EVENT:', self.localid, self.status)

    @staticmethod
    def copy(order):
        return Order(order.exchange_key, order.market, order.symbol, order.order_id, order.localid, order.servertime,order.localtime, order.source, order.status, order.policy, order.method, order.price, order.filled_price, order.amount,order.filled_amount, order.side, order.raw)

    def update(self, feedback: OrderFeedback):
        self.update_weak(feedback)

        self.status = feedback.status or self.status
        self.price = feedback.price or self.price
        self.filled_price = feedback.filled_price or self.filled_price
        self.amount = feedback.amount or self.amount
        self.filled_amount = feedback.filled_amount or self.filled_amount
        self.servertime = feedback.servertime or self.servertime
        self.localtime = feedback.localtime or self.localtime
        self.source = feedback.source or self.source

    def update_weak(self, feedback: OrderFeedback):
        self.policy = self.policy or feedback.policy
        self.localid = self.localid or feedback.localid
        self.method = self.method or feedback.method
        self.price = self.price or feedback.price
        self.amount = self.amount or feedback.amount
        self.side = self.side or feedback.side
        self.source = self.source or feedback.source


class OrderResended(Event):
    def __init__(self, order, new_order):
        super().__init__(order, new_order)
        logger.info(' '.join(['Reordering',str(order.order_id)]))


class Devolve(Event):
    def __init__(self, market, coin, source, devolve_id, amount, devolve_from, devolve_to, localtime, raw):
        super().__init__(market, coin, source, devolve_id, amount, devolve_from, devolve_to, localtime, raw)
        self.market = market
        self.coin = coin
        self.source = source
        self.devolve_id = devolve_id
        self.amount = amount
        self.devolve_from = devolve_from
        self.devolve_to = devolve_to
        self.localtime = localtime
        self.raw = raw
        logger.info(' '.join(['Devolve',market['name']+'_'+coin,str(amount)]))


class PairDict(Event):
    def __init__(self, pair_dict, localtime):
        super().__init__(pair_dict, localtime)
        self.pair_dict = pair_dict
        self.localtime = localtime


class Error(Event):
    def __init__(self, market, symbol, source, errmsg, localtime, raw=None):
        super().__init__(market, symbol, source, errmsg, localtime, raw)
        self.market = market
        self.symbol = symbol
        self.source = source
        self.errmsg = errmsg
        self.localtime = localtime
        self.raw = raw
        # logger.error(' '.join([market['name']+'_'+symbol,'-',errmsg]))


class PendingOrder(Event):
    def __init__(self, raw):
        super().__init__(raw)
        self.raw = raw
