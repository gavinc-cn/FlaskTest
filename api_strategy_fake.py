import time, json, logging
from flask import Flask, request, jsonify
from multiprocessing import RLock
import events




class Ticker:

    def __init__(self):
        self.lastprice = 2


ticker = Ticker()

buy_order = events.OrderFeedback(
    order_id='13213246546',
    filled_price=2,
    filled_amount=4,
)
sell_order = events.OrderFeedback(
    order_id='13213246546',
    filled_price=2,
    filled_amount=6,
)


class APIStrategy:

    def __init__(self):
        self.webserver = None
        self.build_webserver()
        self.identifier = 'future'
        self.general_symbol = 'eos_this_week'
        self.order_dict = {}
        self.lock = RLock()



    def build_webserver(self):
        self.webserver = Flask(__name__)
        # self.webserver.debug = True
        self.webserver.add_url_rule('/send_order', 'send_order', self.send_order_handler, methods=['POST'])
        self.webserver.add_url_rule('/cancel_order', 'cancel_order', self.cancel_order_handler, methods=['POST'])
        self.webserver.add_url_rule('/check_order', 'check_order', self.check_order_handler, methods=['POST'])
        self.webserver.add_url_rule('/maker2taker', 'maker2taker', self.maker2taker_handler, methods=['POST'])
        self.webserver.add_url_rule('/check_profit', 'check_profit', self.check_profit_handler, methods=['POST'])
        self.webserver.add_url_rule('/fix_order', 'fix_order', self.fix_order_handler, methods=['POST'])
        self.webserver.add_url_rule('/fix_market_order', 'fix_market_order', self.fix_market_order_handler, methods=['POST'])

    def started(self, *args):
        self.webserver.run(host='0.0.0.0')
        # base_utils.run_async(self.webserver.run)

    def send_order_handler(self):
        """
        content = {'localid': '123123', 'direction':'open', 'sell_price': '10', 'sell_amount': '2.34', 'buy_price': '2.22', 'buy_amount':
        '10'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        sell_price = content['sell_price']
        sell_amount = content['sell_amount']
        buy_price = content['buy_price']
        buy_amount = content['buy_amount']

        if not isinstance(buy_order, events.OrderFeedback) or not isinstance(sell_order, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'send order failed'})
        result = {'status': True, 'buy_price': buy_price, 'sell_price': sell_price}
        with self.lock:
            self.order_dict.setdefault(localid, {}).setdefault('buy_order', buy_order)
            self.order_dict.setdefault(localid, {}).setdefault('sell_order', sell_order)
        return jsonify(result)

    def cancel_order_handler(self):
        """
        content = {'localid': '123123123', 'action': 'cancell_order'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        # TODO: 在查单以后到撤销操作被交易所执行的时间里，订单可能被成交
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if isinstance(buy_check, events.OrderFeedback) and isinstance(sell_check, events.OrderFeedback):
            if not buy_check.filled_amount and not sell_check.filled_amount:
                buy_cancel = True
                sell_cancel = True
                if buy_cancel and sell_cancel:
                    result = {'status': True}
                else:
                    result = {'status': False, 'errmsg': 'buy_cancel or sell_cancel failed'}
            else:
                result = {'status': False, 'errmsg': 'order has been filled or part-filled'}
        else:
            result = {'status': False, 'errmsg': 'check order failed'}
        return jsonify(result)

    def check_order_handler(self):
        """
        content = {'localid': '123123123'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if not isinstance(buy_check, events.OrderFeedback) or not isinstance(sell_check, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'check order failed'})
        result = {
            'status': True,
            'buy_order': {
                'order_id': buy_check.order_id,
                'price': buy_check.price,
                'filled_price': buy_check.filled_price,
                'amount': buy_check.amount,
                'filled_amount': buy_check.filled_amount,
            },
            'sell_order': {
                'order_id': sell_check.order_id,
                'price': sell_check.price,
                'filled_price': sell_check.filled_price,
                'amount': sell_check.amount,
                'filled_amount': sell_check.filled_amount,
            }
        }
        return jsonify(result)

    def maker2taker_handler(self):
        """
        content = {'localid': '123123123'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if not isinstance(buy_check, events.OrderFeedback) or not isinstance(sell_check, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'check order failed'})
        buy_cancel = True
        sell_cancel = True
        # if not buy_cancel or not sell_cancel:
        #     return jsonify({'status': False, 'errmsg': 'cancel order failed'})
        buy_method = self.order_dict[localid]['buy_order'].method
        sell_method = self.order_dict[localid]['sell_order'].method
        diff = buy_check.filled_amount - sell_check.filled_amount
        if diff > 0:
            new_order = sell_order
        elif diff < 0:
            new_order = buy_order
        else:
            new_order = None
        if isinstance(new_order, events.OrderFeedback):
            with self.lock:
                self.order_dict.setdefault(localid, {}).setdefault('taker_order', new_order)
            result = {'status': True}
        elif isinstance(new_order, events.Error):
            result = {'status': False, 'errmsg': new_order.errmsg}
        elif new_order == None:
            result = {'status': False, 'errmsg': 'No need to send new order'}
        else:
            result = {'status': False, 'errmsg': 'other error'}
        return jsonify(result)

    def check_profit_handler(self):
        """
        content = {'localid': '123123123'}
        :return:
        """
        # TODO 检查是否和期望的一致，如果不一致，需要报警查询原因
        content = request.get_json()
        localid = content['localid']
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if not isinstance(buy_check, events.OrderFeedback) or not isinstance(sell_check, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'check order failed'})

        # if not isinstance(ticker, events.Ticker):
        #     return jsonify({'status': False, 'errmsg': 'check ticker failed'})

        contract_value = 10
        buy_profit = (contract_value / buy_check.filled_price - contract_value / ticker.lastprice) * buy_check.filled_amount if buy_check.filled_amount else 0
        sell_profit = (contract_value / ticker.lastprice - contract_value / sell_check.filled_price) * sell_check.filled_amount if sell_check.filled_amount else 0
        # buy_profit = (now_price - buy_check.filled_price) * buy_check.filled_amount
        profit = buy_profit + sell_profit
        result = {'status': True, 'order_id': localid, 'profit': profit}
        return jsonify(result)

    def fix_order_handler(self):
        """
        content = {'localid': '123123123'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if not isinstance(buy_check, events.OrderFeedback) or not isinstance(sell_check, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'check order failed'})
        # TODO 如果其中一个已成交，导致撤销失败如何处理
        buy_cancel = True
        sell_cancel = True
        # if not buy_cancel or not sell_cancel:
        #     return jsonify({'status': False, 'errmsg': 'cancel order failed'})
        buy_method = self.order_dict[localid]['buy_order'].method
        sell_method = self.order_dict[localid]['sell_order'].method
        diff = buy_check.filled_amount - sell_check.filled_amount
        if diff > 0:
            new_order = sell_order
        elif diff < 0:
            new_order = buy_order
        else:
            new_order = None
        if isinstance(new_order, events.OrderFeedback):
            with self.lock:
                self.order_dict.setdefault(localid, {}).setdefault('taker_order', new_order)
            result = {'status': True}
        elif isinstance(new_order, events.Error):
            result = {'status': False, 'errmsg': new_order.errmsg + ' ' + str(new_order.raw)}
        elif new_order == None:
            result = {'status': False, 'errmsg': 'No need to send new order'}
        else:
            result = {'status': False}
        return jsonify(result)

    def fix_market_order_handler(self):
        """
        content = {'localid': '123123123'}
        :return:
        """
        content = request.get_json()
        localid = content['localid']
        buy_oid = self.order_dict[localid]['buy_order'].order_id
        sell_oid = self.order_dict[localid]['sell_order'].order_id

        buy_check = buy_order
        sell_check = sell_order
        if not isinstance(buy_check, events.OrderFeedback) or not isinstance(sell_check, events.OrderFeedback):
            return jsonify({'status': False, 'errmsg': 'check order failed'})
        # TODO 如果其中一个已成交，导致撤销失败如何处理
        buy_cancel = True
        sell_cancel = True
        # if not buy_cancel or not sell_cancel:
        #     return jsonify({'status': False, 'errmsg': 'cancel order failed'})
        buy_method = self.order_dict[localid]['buy_order'].method
        sell_method = self.order_dict[localid]['sell_order'].method
        diff = buy_check.filled_amount - sell_check.filled_amount
        if diff > 0:
            new_order = sell_order
        elif diff < 0:
            new_order = buy_order
        else:
            new_order = None
        if isinstance(new_order, events.OrderFeedback):
            with self.lock:
                self.order_dict.setdefault(localid, {}).setdefault('taker_order', new_order)
            result = {'status': True}
        elif isinstance(new_order, events.Error):
            result = {'status': False, 'errmsg': new_order.errmsg}
        elif new_order == None:
            result = {'status': False, 'errmsg': 'No need to send new order'}
        else:
            result = {'status': False, 'errmsg': 'other error'}
        return jsonify(result)


if __name__ == "__main__":
    APIStrategy().started()





