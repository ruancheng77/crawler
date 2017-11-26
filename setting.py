#!/usr/bin/env python3
# -*- coding=utf-8 -*-

'''
'''

import os
from rule import Rule

cdir = os.path.dirname(__file__)
home_dir = cdir + "/home"
if not os.path.exists(home_dir):
    os.makedirs(home_dir, mode=0o777, exist_ok=True)
log_dir = home_dir + "/log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, mode=0o777, exist_ok=True)
log_path = log_dir + "/geckodriver.log"
firefox_path = home_dir + "/driver/geckodriver.exe"

# Demo config
# config = {
#     "parser": Rule.PARSER_REQUESTS,
#     "features": Rule.FEATURES_HTML,
#     "site_name": "菜鸟教程",
#     "site_url": "http://www.runoob.com/",
#     "method": Rule.REQUEST_METHOD_GET,
#     "rules": [
#         # 创建爬取 "导航栏" 信息规则（名称、链接）
#         Rule.create(
#             name="ul", 
#             attrs={"id": "index-nav"},
#             rules=[
#                 Rule.create(
#                     name="li", 
#                     all=True, 
#                     rules=[
#                         Rule.create(
#                             name="a", 
#                             all=True, 
#                             data={
#                                     "attrs": [
#                                         {"name": "菜单名称", "value": "text"}, 
#                                         {"name": "链接", "value": "href"}
#                                     ]
#                             }
#                         )
#                     ]
#                 )
#             ]
#         )
#     ]
# }

config = {
    "parser": Rule.PARSER_REQUESTS,
    # "parser": Rule.PARSER_SELENIUM,
    "features": Rule.FEATURES_HTML,
    "site_name": "菜鸟教程",
    "site_url": "http://www.runoob.com/",
    "method": Rule.REQUEST_METHOD_GET,
    "rules": [
        Rule.create(
            name="div", 
            attrs={"class": "codelist"}, 
            all=True, 
            rules=[
                Rule.create(
                    name="h2", 
                    data={
                        "attrs": [
                            {"name": "大标题", "value": "text"}
                        ]
                    }
                ),
                Rule.create(
                    name="a", 
                    attrs={"class": "item-top"}, 
                    all=True, 
                    data={"attrs": [{"name": "小标题链接", "value": "href"}]},
                    rules=[
                        Rule.create("h4", data={"attrs": [{"name": "小标题", "value": "text"}]}),
                        Rule.create("img", data={"attrs": [{"name": "图片链接", "value": "href"}]}),
                        Rule.create("strong", data={"attrs": [{"name": "说明", "value": "text"}]})
                    ]
                )
            ]
        )
    ]
}