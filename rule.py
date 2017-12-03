#!/usr/bin/env python3
# -*- coding=utf-8 -*-



class Rule(object):
    
    PARSER_SELENIUM = "selenium"
    PARSER_REQUESTS = "requests"

    FEATURES_HTML = "html.parser"
    FEATURES_JSON = "json.parser"

    REQUEST_METHOD_GET = "get"
    REQUEST_METHOD_POST = "post"
    REQUEST_METHOD_HEAD = "head"
    REQUEST_METHOD_PUT = "put"
    REQUEST_METHOD_DELETE = "delete"
    REQUEST_METHOD_OPTIONS = "options"

    TYPE_BEAUTIFUL_SOUP = "beautifulSoup"
    TYPE_REGX = "regx"

    @staticmethod
    def create(rule_type=None, name=None, attrs=None, all=None, data=None, rules=None):
        '''
        参数说明：
        - :rule_type(String):   子规则默认会继承父规则的 rule_type
            >- BeautifulSoup(默认)
            >- Regx
        - :name(String):
            >- 当 rule_type=Rule.TYPE_BEAUTIFUL_SOUP 时：
                >>- name 表示 dom 节点名称
            >- 当 rule_type=Rule.TYPE_REGX 时：
                >>- name 表示正则表达式获取对象的名称
        - :attrs(Dict):
            >- 当 rule_type=Rule.TYPE_BEAUTIFUL_SOUP 时：
                >>- attrs 表示获取 dom 节点的 {"属性" : "属性值"}的字典集合
        - :all(Boolean):
            >- 当 rule_type=Rule.TYPE_BEAUTIFUL_SOUP 时：
                >>- :True: 表示查找所有
                >>- :False: 表示只查找一个
        - :data(Dict):
            >- 当 rule_type=Rule.TYPE_BEAUTIFUL_SOUP 时：
                >>- data 表示获取数据的配置项字典集合
                >>- attrs(List): 从当前 dom 节点获取需要的数据, 格式如下：\n 
        {"name": "链接", "value": "href"} \n
        当 value 等于 text 或者 string 时，表示获取当前 dom 节点的文本。
        当 value 等于 dom 节点属性的时候，表示获取当前 dom 节点的属性值。

        - :rules(List):     以当前 dom 节点为父节点创建查找规则。
        '''
        
        if rule_type is None:
            rule_type = Rule.TYPE_BEAUTIFUL_SOUP
        if all is None:
            all = False
        if rules:
            for rule in rules:
                if rule.get("rule_type") is None:
                    rule["rule_type"] = d["rule_type"]
        return Rule.__getattribute__(Rule, rule_type)(Rule, name, attrs, all, data, rules)

    def _set_rule_type(self, rule_type, rules):
        for rule in rules:
            if rule.get("rule_type") is None:
                rule["rule_type"] = rule_type
            if rule.get("rules"):
                self._set_rule_type(Rule, rule_type, rule.get("rules"))

    def beautifulSoup(self, name=None, attrs=None, all=None, data=None, rules=None):
        d = {}
        d["rule_type"] = Rule.TYPE_BEAUTIFUL_SOUP
        d["name"] = name
        d["attrs"] = attrs
        d["all"] = all
        d["data"] = data
        if rules:
            self._set_rule_type(Rule, Rule.TYPE_BEAUTIFUL_SOUP, rules)
        d["rules"] = rules
        return d

    def regx(self, name=None, attrs=None, all=None, data=None, rules=None):
        d = {}
        d["rule_type"] = Rule.TYPE_REGX
        d["name"] = name
        d["attrs"] = attrs
        d["all"] = all
        d["data"] = data
        if rules:
            self._set_rule_type(Rule, Rule.TYPE_BEAUTIFUL_SOUP, rules)
        d["rules"] = rules
        return d

if __name__ == '__main__':
    rule = Rule.create(
        name="ul", 
        attrs={"class": "middle-column-home"}, 
        data={"attrs": [{"name": "name", "value": "href"}]}, 
        rules=[
            Rule.create(name="li", attrs={"id": "menu"}, rules=[Rule.create(name="li", attrs={"id": "menu"})])
        ]
    )
    print(rule)
    