#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory,Host,Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
import os
import sys
import json


class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi2(object):
    def __init__(self):
        self.host_info_dic = {
            'dbservers': {
                # 'hosts': ['oggsource', 'oggtarget','bindesktop'],
                'hosts': ['oggsource01', 'oggtarget01', 'bindesktop01'],
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
        self.Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])
        self.variable_manager = VariableManager()
        self.loader = DataLoader()

        self.options = self.Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False)
        self.passwords = {}
        self.host_list = ['oggsource01', 'oggtarget01','bindesktop01']
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,host_list=[])
        self.init_inventory()
        self.variable_manager.set_inventory(self.inventory)
        self.results_callback = ResultsCollector()


    def init_inventory(self):
        for  k, v in self.host_info_dic.items():
            if k != '_meta':
                group_name = k
                group_dic = v
                group = Group(name=group_name)
                for host_name in v['hosts']:
                    host = Host(name=host_name)
                    host.set_variable('ansible_ssh_host', host_name)
                    host.set_variable('ansible_ssh_user', self.host_info_dic['_meta']['hostvars'][host_name]['ansible_ssh_user'])
                    host.set_variable('ansible_ssh_pass', self.host_info_dic['_meta']['hostvars'][host_name]['ansible_ssh_pass'])
                    group.add_host(host)
                self.inventory.add_group(group)

        # print self.inventory.get_group_dict()



    def run_module(self):
        play_source = dict(
            name="Ansible Play",
            hosts=self.host_list,
            gather_facts='no',
            tasks=[
                # dict(action=dict(module='ls')),
                dict(action=dict(module='raw',args='touch /tmp/aaa'))
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        qm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            tqm._stdout_callback = self.results_callback
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()



    def run_playbook(self):

        """
              run ansible palybook
              """
        extra_vars = {}  # 额外的参数 sudoers.yml以及模板中的参数，它对应ansible-playbook test.yml --extra-vars "host='aa' name='cc' "
        host_list_str = ','.join([item for item in self.host_list])
        extra_vars['host_list'] = host_list_str
        playbook_path = 'test.yml'  # modify here, change playbook
        self.variable_manager.extra_vars=extra_vars
        # variable_manager.extra_vars = {"test": "pong111111111111111",} # modify here, This can accomodate various other command line arguments.`
        if not os.path.exists(playbook_path):
            print '[INFO] The playbook does not exist'
            sys.exit()

        passwords = {}

        executor = PlaybookExecutor(
            playbooks=[playbook_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=passwords
        )

        executor._tqm._stdout_callback = self.results_callback
        executor.run()

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        return self.results_raw

if __name__ == '__main__':
    ansible_handler = AnsibleApi2()
    ansible_handler.run_playbook()
    print ansible_handler.get_result()