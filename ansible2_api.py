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
import ConfigParser
from ConfigParser import DEFAULTSECT


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
        self.tags_str = 'start,stop'
        self.host_file_path = 'hosts/all-hosts'
        self.Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax','tags'])

        self.options = self.Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False,tags=self.tags_str)

        # self.Options = namedtuple('Options', ['listhosts', 'listtasks','forks', 'become', 'become_method', 'become_user', 'check'])
        # self.options = self.Options(listhosts=False, listtasks=True, forks=10, become=None, become_method=None, become_user='root', check=False)


        self.variable_manager = VariableManager()
        self.loader = DataLoader()

        # self.variable_manager.add_group_vars_file()

        self.passwords = {}
        self.host_list = ['server02',]
        self.group_var_file_path = 'group_vars/all'
        # self.group_var_file_path = 'group_vars/all_84'

        self.variable_manager.add_group_vars_file(self.group_var_file_path,self.loader)
        # print self.variable_manager._group_vars_files
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,host_list=self.host_file_path)
        # self.init_inventory()
        self.variable_manager.set_inventory(self.inventory)
        self.results_callback = ResultsCollector()




    def run_module(self):
        play_source = dict(
            name="Ansible Play",
            hosts=self.host_list,
            gather_facts='no',
            tasks=[
                # dict(action=dict(module='ls')),
                dict(action=dict(module='raw',args='touch /tmp/ccc'))
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
        playbook_path = 'test.yml'  # modify here, change playbook
        print host_list_str
        extra_vars["host_list"] = host_list_str
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
            passwords=passwords,
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


class KconfigParser(ConfigParser.RawConfigParser):


    def read_config(self,config_file_path):
        data = {}
        self.read(config_file_path)
        sections = self._sections
        for section in sections:
            data[section] = {}
            for var in sections[section].items():
                if var[0] == '__name__':continue
                data[section][var[0]] = var[1].split()

        return data




#
# def compare_input_app_with_common_config(apps_list,result_dict):
#
#     config = KconfigParser()
#     app_config_dict = config.read_config(app_config_file_path)
#     java_apps_list = app_config_dict['java_and_web_catalog']['javaapps']
#     web_apps_list = app_config_dict['java_and_web_catalog']['webapps']
#     result_dict['apply_java_apps'] = []
#     result_dict['apply_web_apps'] = []
#     for var in apps_list:
#         if var in java_apps_list:
#             result_dict['apply_java_apps'].append(var)
#         elif var in web_apps_list:
#             result_dict['apply_web_apps'].append(var)




if __name__ == '__main__':
    ansible_handler = AnsibleApi2()
    ansible_handler.run_playbook()
    print ansible_handler.get_result()
    # if len(sys.argv) != 4:
    #     print 'Please input the right parameter !'
    #     print sys.argv
    #     sys.exit(1)
    #
    # apps_str = sys.argv[1]
    # operation = sys.argv[2]
    # env_id = sys.argv[3]
    # app_config_file_path = 'common.properties'
    #
    #
    # apps_list = apps_str.split(',')
    # apply_app_dict = {}
    #
    #
    # compare_input_app_with_common_config(apps_list,apply_app_dict)
    # print apply_app_dict
    #
    #
