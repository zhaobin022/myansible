#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
基于Python的动态Inventory脚本举例
'''

import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json


class ExampleInventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        self.host_info_dic = {
            'dbservers': {
                # 'hosts': ['oggsource', 'oggtarget','bindesktop'],
                'hosts': ['oggsource01', 'oggtarget01','bindesktop01'],
                # 'vars': {
                #     'ansible_ssh_user': 'vagrant',
                #     'ansible_ssh_private_key_file':
                #         '~/.vagrant.d/insecure_private_key',
                #     'example_variable': 'value'
                # }
            },
            '_meta': {
                'hostvars': {
                    'oggsource01': {
                        "ansible_ssh_user": "root",
                        "ansible_ssh_pass": "rootroot"
                    },
                    'oggtarget01': {
                        "ansible_ssh_user": "root",
                        "ansible_ssh_pass": "rootroot"
                    },
                    'bindesktop01': {
                        "ansible_ssh_user": "root",
                        "ansible_ssh_pass": "123abc,.",
                        "a": "b"
                    }
                }
            }
        }

        # 定义`--list`选项
        if self.args.list:
            self.inventory = self.example_inventory()
        # 定义`--host [hostname]`选项
        elif self.args.host:
        # 未部署，我们这里只演示--list选项功
            if self.host_info_dic['_meta']['hostvars'].has_key(self.args.host):
                self.inventory = self.host_info_dic['_meta']['hostvars'][self.args.host]
            else:

                self.inventory = self.empty_inventory()

        # 如果没有主机组或变量要设置，就返回一个空Inventory
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # 用于展示效果的JSON格式的Inventory文件内容
    def example_inventory(self):
        return self.host_info_dic

    # 返回仅用于测试的空Inventory


    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

        # 读取并分析读入的选项和参数


    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


ExampleInventory()
