#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2016年12月22日
@author: victor
@see: collect configs in *.ini files .
'''
from configobj import ConfigObj
class Config(object):
    '''
    读取ini文件，获取配置参数
    '''

    def __init__(self, path):
        self.path = path
        self.config = ConfigObj(self.path, encoding='UTF-8')

    def get(self, option):
        param = dict()
        try:
            for key in self.config[option]:
                param[key] = self.config[option][key]
        except:
            print '文件中不存在option：%' % (option)
        return param

    def sections(self):
        return self.config.sections

    def set(self, option, key, value):
        self.config[option][key] = value
        self.config.write()


if __name__ == '__main__':
    conf = Config('./db.ini')
    print conf.get('mysql')