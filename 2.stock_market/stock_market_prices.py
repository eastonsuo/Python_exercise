# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
from colorama import init, Fore, Back, Style


start_date = "2018-02-09"
end_date = "2018-02-09"

import xlrd
import json
import time
xl_data = xlrd.open_workbook('pool_2018-01-29.xlsx')
table = xl_data.sheet_by_index(0)
stock_name = table.col_values(0)[1:]
stock_list = table.col_values(1)[1:]
aim1_price = table.col_values(2)[1:]
aim2_price = table.col_values(3)[1:]
aim3_price = table.col_values(4)[1:]
recommend = table.col_values(5)[1:]


def sina_now():

    error_list = []
    for (
            name,
            stock,
            aim1,
            aim2,
            aim3,
            r) in zip(
            stock_name,
            stock_list,
            aim1_price,
            aim2_price,
            aim3_price,
            recommend):

        # url = http://hq.sinajs.cn/list=sh601006
        try:
            time.sleep(5)
            request = urllib2.Request(url)
            request.add_header('Authorization', 'APPCODE ' + appcode)
            response = urllib2.urlopen(request)
            content = response.read()
            if (content):
                content = json.loads(content)
                price = content["showapi_res_body"]["list"][0]["close_price"]
                str = u"名称:%s|代码:%s|收盘价:%s|建仓线:%s|加仓线:%s|重仓线:%s" % (
                    name, stock, price, aim1, aim2, aim3)
                if price < aim1:
                    print(Back.GREEN + str)
                else:
                    if r > 0:
                        print(Fore.RED + str)
                    else:
                        print(Fore.BLACK + str)
        except Exception as e:
            print(u"error when requiring %s(%s)" % (name, stock))
            print(u"e_message :%s " % e.message)
            time.sleep(60)
            error_list.append(stock)
    print(error_list)


def ali(list=None):
    host = 'http://stock.market.alicloudapi.com'
    path = '/sz-sh-stock-history'
    method = 'GET'
    appcode = 'your_code'
    error_list = []
    for (
            name,
            stock,
            aim1,
            aim2,
            aim3,
            r) in zip(
            stock_name,
            stock_list,
            aim1_price,
            aim2_price,
            aim3_price,
            recommend):
        querys = 'begin=%s&code=%s&end=%s' % (start_date, stock, end_date)
        bodys = {}
        url = host + path + '?' + querys
        try:
            if list:
                if stock not in list:
                    continue
            time.sleep(5)
            request = urllib2.Request(url)
            request.add_header('Authorization', 'APPCODE ' + appcode)
            response = urllib2.urlopen(request)
            content = response.read()
            if (content):
                content = json.loads(content)
                price = content["showapi_res_body"]["list"][0]["close_price"]
                str = u"名称:%s|代码:%s|收盘价:%s|建仓线:%s|加仓线:%s|重仓线:%s" % (
                    name, stock, price, aim1, aim2, aim3)
                if float(price) < float(aim1):
                    print(Fore.GREEN + str)
                else:
                    if r > 0:
                        print(Fore.RED + str)
                    else:
                        print(Fore.BLACK + str)
        except Exception as e:
            print(u"error when requiring %s(%s)" % (name, stock))
            time.sleep(60)
            error_list.append(stock)
    print(error_list)
    return error_list


if __name__ == '__main__':
    error_list = ali()
    ali(error_list)
