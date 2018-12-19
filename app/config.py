#-*- encoding: utf-8 -*-

import os

app_config = {

    # 系统版本号
    'version': '0.0.1',
    # 站点名称
    'site_name': '云海微信服务',

    # 站点域名
    'site_host': 'http://soc-wx-service.ejyi.com/',

}

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    #系统调试模式，服务器可设置为 False
    debug=True,
)