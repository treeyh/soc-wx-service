# -*- encoding: utf-8 -*-

import tornado.web
# import tornado.escape
from tornado.escape import url_escape
from datetime import datetime

import config
from common import result_info
import copy


class BaseHandler(tornado.web.RequestHandler):

    def get_ok_and_back_params(self, ps, refUrl=''):
        ps['msg'] = result_info.ResultInfo.get(0, '')
        ps['gotoUrl'] = refUrl
        return ps

    def get_header(self, name, default=None):
        return self._headers.get(name, default)

    # def get_arg(self, key, default=None, strip=True):
    #     val = self.get_argument(key, default, strip)
    #     if val != None and isinstance(val, unicode):
    #         val = val.encode('utf-8')
    #     return val

    def get_args(self, ls=[], default=None, map={}):
        for l in ls:
            map[l] = self.get_arg(l, default)
        return map

    def out_fail(self, code, msg=None, jsoncallback=None):
        if None != msg and '' != msg:
            msg = '%s,%s' % (result_info.ResultInfo.get(code, ''), msg)
        else:
            msg = result_info.ResultInfo.get(code, '')
        j = '{"code":%d,"msg":"%s"}' % (code, msg.replace('"', '\\"'))
        if jsoncallback == None or jsoncallback == '':
            self.write(j)
        else:
            self.write('%s(%s)' % (jsoncallback, j))

    # def out_ok(self, data=None, jsoncallback=None):
    #     if data == None or data == '':
    #         j = '{"code":0,"msg":"OK"}'
    #     elif str == type(data) or unicode == type(data):
    #         j = '{"code":0,"msg":"OK","data":%s}' % data
    #     else:
    #         j = '{"code":0,"msg":"OK","data":%s}' % str_helper.json_encode(data)
    #     if jsoncallback == None or jsoncallback == '':
    #         self.write(j)
    #     else:
    #         self.write('%s(%s)' % (jsoncallback, j))

    # def check_str_empty_input(self, map={}, ls=[]):
    #     error = ''
    #     for l in ls:
    #         if str_helper.is_null_or_empty(map[l]):
    #             error = '%s %s,' % (error, l)
    #     if str_helper.is_null_or_empty(error) == False:
    #         error = error + result_info.ResultInfo.get(1001, '')
    #     return error

    def format_none_to_empty(self, obj):
        if isinstance(obj, dict):
            for key in obj.keys():
                if isinstance(obj[key], dict) or isinstance(obj[key], list):
                    self.format_none_to_empty(obj[key])
                elif obj[key] == None:
                    obj[key] = ''
        elif isinstance(obj, list):
            for key in obj:
                if isinstance(key, dict) or isinstance(key, list):
                    self.format_none_to_empty(key)
                elif key == None:
                    key = ''
        return obj