#   crawler（爬虫工程）
采用配置化的爬虫工程，只需要配置信息，即可抓取网站信息。

## 所需第三方包
    1.bs4
    2.selenium
    3.requests

##  setting.py 配置示例

1.使用 selenium 抓取菜鸟教程菜单信息

    config = {
        "parser": Rule.PARSER_SELENIUM,
        "features": Rule.FEATURES_HTML,
        "site_name": "菜鸟教程",
        "site_url": "http://www.runoob.com/",
        "method": Rule.REQUEST_METHOD_GET,
        "rules": [
            # 创建爬取 "导航栏" 信息规则（名称、链接）
            Rule.create(
                name="ul", 
                attrs={"id": "index-nav"},
                rules=[
                    Rule.create(
                        name="li", 
                        all=True, 
                        rules=[
                            Rule.create(
                                name="a", 
                                all=True, 
                                data={
                                        "attrs": [
                                            {"name": "菜单名称", "value": "text"}, 
                                            {"name": "链接", "value": "href"}
                                        ]
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    }

2.使用 requests 解析 JSON 数据示例

    config = {
        "parser": Rule.PARSER_REQUESTS,
        "features": Rule.FEATURES_JSON,
        "site_name": "测试",
        "site_url": "http://localhost:9090/api/user/1",
        "method": Rule.REQUEST_METHOD_POST,
        "rules": [
            Rule.create(
                data={
                    "attrs": [
                        {
                            "name": "响应状态", 
                            "value": "status"
                        },
                        {
                            "name": "响应消息", 
                            "value": "msg"
                        },
                        {
                            "name": "响应时间戳", 
                            "value": "timestamp"
                        },
                        {
                            "name": "响应结果", 
                            "value": "result", 
                            "attrs": [
                                {
                                    "name": "响应数据", 
                                    "value": "data", 
                                    "attrs":[
                                        {"name": "主键", "value": "id"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            )
        ]
    }

3.将抓取数据存储到文件


    file_path = home_dir + "/data/data.txt"
    config = {
        "parser": Rule.PARSER_REQUESTS,
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
                            "file": file_path,
                            "attrs": [
                                {"name": "大标题", "value": "text"}
                            ]
                        }
                    ),
                    Rule.create(
                        name="a", 
                        attrs={"class": "item-top"}, 
                        all=True, 
                        data={
                            "file": file_path,
                            "attrs": [
                                {"name": "小标题链接", "value": "href"}
                            ]
                        },
                        rules=[
                            Rule.create("h4", data={"file": file_path,"attrs": [{"name": "小标题", "value": "text"}]}),
                            Rule.create("img", data={"file": file_path,"attrs": [{"name": "图片链接", "value": "href"}]}),
                            Rule.create("strong", data={"file": file_path,"attrs": [{"name": "说明", "value": "text"}]})
                        ]
                    )
                ]
            )
        ]
    }