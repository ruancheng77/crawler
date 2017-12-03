#!/usr/bin/env python3
# -*- coding=utf-8 -*-

'''
配置文件
'''

import os
import sys
from rule import Rule

def mkdir(d):
    '如果目录不存在，则创建目录'
    if not os.path.exists(d):
        os.makedirs(d, mode=0o777, exist_ok=True)

# 当前目录
cdir = os.path.dirname(os.path.abspath(__file__))
# 指定 home 目录
home_dir = cdir + "/home"
mkdir(home_dir)
# 指定 log 目录
log_dir = home_dir + "/log"
mkdir(log_dir)
# 指定驱动执行输出的日志文件路径
log_path = log_dir + "/geckodriver.log"
# 指定火狐浏览器驱动的文件路径
firefox_path = home_dir + "/driver/geckodriver.exe"

# 指定抓取数据保存文件
file_path = home_dir + "/data/data.txt"

menu_a = Rule.create(name="a", data={"file": file_path, "attrs": [{"name": "菜单名称", "value": "text"},{"name": "菜单链接", "value": "href"}]})
menu_li = Rule.create(name="li", all=True, rules=[menu_a])
menu_ul = Rule.create(rule_type=Rule.TYPE_BEAUTIFUL_SOUP, name="ul", attrs={"id": "index-nav"}, rules=[menu_li])

config = {
    "parser": Rule.PARSER_REQUESTS,
    "features": Rule.FEATURES_HTML,
    "site_name": "菜鸟教程",
    "site_url": "http://www.runoob.com/",
    "method": Rule.REQUEST_METHOD_GET,
    "rules": [menu_ul]
}