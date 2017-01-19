#!/usr/bin/python
import sys
import json
import shlex
import commands
import re



print json.dumps({
    "changed": False,
    "ansible_facts": {
        "ansible_private_ipv4_address": 'lalala111111111111111111111111'
    }
})