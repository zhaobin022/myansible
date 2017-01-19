#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

try:
    import json
except ImportError:
    import simplejson as json

'''这里是模拟数据，工作上一般该数据都是从数据库或者缓存中读取的'''
mockData = {
    "dbservers": {
        "hosts": ["oggsource","oggtarget"],
        "vars":{
                "ansible_ssh_user":"root",
                "ansible_ssh_pass":"rootroot"
        }
    }
}
'''模拟数据结束'''


def getList():
    '''get list hosts group'''
    print json.dumps(mockData)


def getVars(host):
    '''Get variables about a specific host'''
    print json.dumps(mockData[host]["vars"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', dest='list', help='get all hosts')
    parser.add_argument('--host', action='store', dest='host', help='get all hosts')
    args = parser.parse_args()

    if args.list:
        getList()

    if args.host:
        getVars(args.host)