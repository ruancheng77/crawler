#!/usr/bin/env python3
# -*- coding=utf-8 -*-

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
        parser = self.get_parser()
        page_source = parser()
        self.resolve_page_source(page_source)
    
    def get_parser(self):
        return self.__getattribute__("by_" + self.parser)

    def get_soup(self, page_source):
        return BeautifulSoup(page_source, self.features)

    def by_selenium(self):
        from selenium import webdriver
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
        import requests
        try:
            response = requests.request(method=self.method, url=self.site_url)
            page_source = response.content.decode()
            return page_source
        except Exception as e:
            print("Error >>> ", e)
        finally:
            pass

    def handler_rules(self, source, rules, parent=None):
        source = parent or source
        for rule in rules:
            if rule.get("all") == False:
                self.handler_rule_single(source, rule)
            elif rule.get("all") == True:
                self.handler_rule_multi(source, rule)

    def handler_rule_single(self, source, rule, parent=None):
        source = parent or source
        tag = source.find(name=rule["name"], attrs=rule["attrs"])
        if tag:
            if rule.get("data"):
                self.resolve_data(tag, rule.get("data"))
            if rule.get("rules"):
                self.handler_rules(source, rule.get("rules"), tag)
    
    def handler_rule_multi(self, source, rule, parent=None):
        source = parent or source
        tags = source.find_all(name=rule.get("name"), attrs=rule.get("attrs"))
        if tags:
            if rule.get("data"):
                for tag in tags:
                    self.resolve_data(tag, rule.get("data"))
                    if rule.get("rules"):
                        self.handler_rules(source, rule.get("rules"), tag)
            else:
                if rule.get("rules"):
                    for tag in tags:
                        self.handler_rules(source, rule.get("rules"), tag)

    def resolve_page_source(self, page_source):
        soup = self.get_soup(page_source)
        self.handler_rules(soup, self.rules)

    def resolve_data(self, tag, data):
        content = {}
        if data.get("attrs"):
            for attr in data.get("attrs"):
                name = attr.get("name")
                value = attr.get("value")
                if value == "text" or value == "string":
                    value = tag.__getattribute__(value)
                else:
                    value = tag.get(value)
                print("%s >>> %s"%(name, value))

if __name__ == "__main__":
    crawler = Crawler(**setting.config)
    crawler.run()
