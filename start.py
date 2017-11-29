#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import json
import os

from bs4 import BeautifulSoup

import setting
from rule import Rule


class Crawler(object):
    '''
    参数说明：
    - :site_name: 站点名称
    - :site_url: 站点url
    - :method: 请求方法("GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE")
    - :rending: 是否需要渲染
    - :rules: 爬取所需信息的规则
      >>>  ID = "id"
      >>>  XPATH = "xpath"
      >>>  LINK_TEXT = "link text"
      >>>  PARTIAL_LINK_TEXT = "partial link text"
      >>>  NAME = "name"
      >>>  TAG_NAME = "tag name"
      >>>  CLASS_NAME = "class name"
      >>>  CSS_SELECTOR = "css selector"
    '''

    def __init__(self, parser=None, features=None, site_name=None, site_url=None, method=None, rules=None,
         *args, **kwargs):
        self.parser = parser or Rule.PARSER_REQUESTS
        self.features = features or Rule.FEATURES_HTML
        self.site_name = site_name
        self.site_url = site_url
        self.method = method if method else Rule.REQUEST_METHOD_GET
        self.rules = rules

    def run(self):
        '执行方法'
        parser = self.get_parser()
        source = self.resolve_source(parser())
        self.handler_source(source)
    
    def get_parser(self):
        '获取对应的解析方法'
        return self.__getattribute__("by_" + self.parser)


    def by_selenium(self):
        '使用 selenium 获取数据'
        try:
            from selenium import webdriver
        except Exception as e:
            print(e)
            return
        try:
            driver = webdriver.Firefox(
                executable_path=setting.firefox_path, log_path=setting.log_path)
            driver.get(self.site_url)
            return driver.page_source
        except Exception as e:
            print("Error >>> ", e)
        finally:
            if driver:
                driver.close()

    def by_requests(self):
        '使用 requests 获取数据'
        try:
            import requests
        except Exception as e:
            print(e)
            return
        try:
            response = requests.request(method=self.method, url=self.site_url)
            page_source = response.content.decode()
            return page_source
        except Exception as e:
            print("Error >>> ", e)
        finally:
            pass

    def resolve_source(self, source):
        '解析数据源'
        if self.features == Rule.FEATURES_HTML:
            return BeautifulSoup(source, self.features)
        elif self.features == Rule.FEATURES_JSON:
            return json.loads(source)
    
    def handler_source(self, source):
        '处理数据源'
        if self.features == Rule.FEATURES_HTML:
            self.handler_html(source)
        elif self.features == Rule.FEATURES_JSON:
            self.handler_json(source)
    
    def handler_html(self, source):
        '处理 html 页面资源'
        self.handler_html_rules(source, self.rules)

    def handler_json(self, source):
        '处理 json 数据'
        self.handler_json_rules(source, self.rules)

    def handler_html_rules(self, source, rules, parent=None):
        '处理 html 类型规则'
        source = parent or source
        for rule in rules:
            if rule.get("all") == False:
                self.handler_rule_single(source, rule)
            elif rule.get("all") == True:
                self.handler_rule_multi(source, rule)

    def handler_json_rules(self, source, rules):
        '处理 json 类型规则'
        for rule in rules:
            self.resolve_data(source, rule)

    def handler_rule_single(self, source, rule, parent=None):
        '处理单对象规则'
        source = parent or source
        tag = source.find(name=rule["name"], attrs=rule["attrs"])
        if tag:
            if rule.get("data"):
                self.resolve_data(tag, rule)
            if rule.get("rules"):
                self.handler_html_rules(source, rule.get("rules"), tag)
    
    def handler_rule_multi(self, source, rule, parent=None):
        '处理多对象规则'
        source = parent or source
        tags = source.find_all(name=rule.get("name"), attrs=rule.get("attrs"))
        if tags:
            if rule.get("data"):
                for tag in tags:
                    self.resolve_data(tag, rule)
                    if rule.get("rules"):
                        self.handler_html_rules(source, rule.get("rules"), tag)
            else:
                if rule.get("rules"):
                    for tag in tags:
                        self.handler_html_rules(source, rule.get("rules"), tag)

    def resolve_data(self, source, rule):
        '解析数据'
        data = rule.get("data")
        if data:
            if self.features == Rule.FEATURES_HTML:
                if data.get("attrs"):
                    self.resolve_html_attrs(source, data)
            elif self.features == Rule.FEATURES_JSON:
                if data.get("attrs"):
                    self.resolve_json_attrs(source, data)
    
    def resolve_html_attrs(self, source, data):
        '解析 html 属性'
        attrs = data.get("attrs")
        for attr in attrs:
            name = attr.get("name")
            value = attr.get("value")
            if value == "text" or value == "string":
                value = source.__getattribute__(value)
            else:
                value = source.get(value)
            # print(name, value)
            if data.get("file"):
                self.save_data_file(data.get("file"), name, value)

    def resolve_json_attrs(self, source, data):
        '解析 json 属性'
        attrs = data.get("attrs")
        for attr in attrs:
            name = attr.get("name")
            value = attr.get("value")
            value = source.get(value)
            if attr.get("attrs"):
                self.resolve_json_attrs(value, attr)
            else:
                print("%s >>> %s"%(name, value))

    def save_data_file(self, fp, name, value):
        fd = os.path.dirname(fp)
        if not os.path.exists(fd):
            setting.mkdir(fd)
        with open(fp, "a") as f:
            json.dump({"name": name, "value": value}, f)
            f.write("\n")

if __name__ == "__main__":
    crawler = Crawler(**setting.config)
    crawler.run()
