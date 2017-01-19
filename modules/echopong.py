#!/usr/bin/python

import json
import commands
import re
from ansible.module_utils.basic import *
from ansible.module_utils.facts import *

def get_ansible_private_ipv4_address():
    iprex = "(^192\.168)|(^10\.)|(^172\.1[6-9])|(^172\.2[0-9])|(^172\.3[0-1])"
    output = commands.getoutput("""/sbin/ifconfig |grep "Link encap" |awk '{print $1}' |grep -wv 'lo'""")
    nics = output.split('\n')
    for i in nics:
        ipaddr = commands.getoutput("""/sbin/ifconfig %s |grep -w "inet addr" |cut -d: -f2 | awk '{print $1}'""" % (i))
        if re.match(iprex,ipaddr):
            ansible_private_ipv4_address = ipaddr
            return ansible_private_ipv4_address

def main():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            get_facts=dict(default="yes", required=False),
            args=dict(required=True)
        ),
        supports_check_mode = True,
    )

    ansible_facts_dict = {
        "changed" : False,
        "rc": 0,
        "ansible_facts": {
            }
    }

    if module.params['get_facts'] == 'yes':
        ansible_private_ipv4_address = get_ansible_private_ipv4_address()
        ansible_facts_dict['ansible_facts']['ansible_private_ipv4_address'] = ansible_private_ipv4_address
        ansible_facts_dict['ansible_facts']['args'] = module.params['args']

    print json.dumps(ansible_facts_dict)


main()