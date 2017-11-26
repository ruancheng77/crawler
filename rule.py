#!/usr/bin/env python3
# -*- coding=utf-8 -*-



class Rule(object):
    
    PARSER_SELENIUM = "selenium"
    PARSER_REQUESTS = "requests"

    FEATURES_HTML = "html.parser"
    
    NAME_ID = "id"
    NAME_XPATH = "xpath"
    NAME_LINK_TEXT = "link text"
    NAME_PARTIAL_LINK_TEXT = "partial link text"
    NAME_NAME = "name"
    NAME_TAG_NAME = "tag name"
    NAME_CLASS_NAME = "class name"
    NAME_CSS_SELECTOR = "css selector"

    REQUEST_METHOD_GET = "get"
    REQUEST_METHOD_POST = "post"
    REQUEST_METHOD_HEAD = "head"
    REQUEST_METHOD_PUT = "put"
    REQUEST_METHOD_DELETE = "delete"
    REQUEST_METHOD_OPTIONS = "options"

    @staticmethod
    def create(name=None, attrs=None, all=None, data=None, rules=None):
        '''
        参数说明：
        - :name(String):    dom 节点名称
        - :attrs(Dict):     dom 节点属性值
        - :all(Boolean):    True: 查找所有，False：查找第一个
        - :data(Dict):      
            >- attrs(List): 
            从当前 dom 节点获取需要的数据, 格式如下：\n 
        {"name": "链接", "value": "href"} \n
        当 value 等于 text 或者 string 时，表示获取当前 dom 节点的文本。
        当 value 等于 dom 节点属性的时候，表示获取当前 dom 节点的属性值。

        - :rules(List):     以当前 dom 节点为父节点创建查找规则。
        '''
        d = {}
        d["name"] = name
        d["attrs"] = attrs
        d["all"] = False if all is None else all
        d["data"] = data
        d["rules"] = rules
        return d

if __name__ == '__main__':
    Rule.create("div", {"class": "middle-column-home"}, Rule.TYPE_SINGLE)
    