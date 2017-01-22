#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import json
import ConfigParser
from ConfigParser import DEFAULTSECT

class KconfigParser(ConfigParser.RawConfigParser):
    def write(self, fp):
        """解决ConfigParser的冒号被自动保存为等号而引起的后续解析问题"""
        # if self._defaults:
        #     fp.write("[%s]\n" % DEFAULTSECT)
        #     for (key, value) in self._defaults.items():
        #         fp.write("%s: %s\n" % (key, str(value).replace('\n', '\n\t')))
        #     fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s: %s\n" %
                             (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")


    def read_hosts(self,fp):

        data = []

        self.read(fp)
        sections = self._sections
        for section in sections:
            group_dic = {"group":section,"items":[]}
            host_list = sections[section].items()



            for host_info in host_list:
                host_dic = {}
                if host_info[0] == '__name__':continue
                host_dic["name"] = host_info[0]
                for var_str in host_info[1].split():
                    k,v = var_str.split("=")
                    if k == 'ansible_ssh_port':
                        host_dic["ssh_port"] = int(v)
                    elif k == 'ansible_ssh_host':
                        host_dic["ssh_host"] = v
                    elif k == 'ansible_ssh_user':
                        host_dic["ssh_user"] = v
                    elif k == 'ansible_ssh_pass':
                        host_dic["ssh_password"] = v
                group_dic["items"].append(host_dic)

            data.append(group_dic)
        return data




class Generate_ansible_hosts(object):
    def __init__(self, host_file):
        self.config = KconfigParser(allow_no_value=True)
        self.host_file = host_file


    def read_host_file(self):
        self.config = KconfigParser(allow_no_value=True)

        return self.config.read_hosts(self.host_file)


    def create_all_servers(self, items):
        self.config = KconfigParser(allow_no_value=True)
        for i in items:
            group = i['group']
            self.config.add_section(group)
            for j in i['items']:
                name = j['name']
                ssh_port = j['ssh_port']
                ssh_host = j['ssh_host']
                ssh_user = j['ssh_user']
                ssh_password = j['ssh_password']
                build = "ansible_ssh_port={0} ansible_ssh_host={1} ansible_ssh_user={2} ansible_ssh_pass={3}".format(
                        ssh_port, ssh_host, ssh_user,ssh_password)
                self.config.set(group, name, build)
        with open("gen_hosts_test", 'wb') as configfile:
            self.config.write(configfile)
        return True

if __name__ == '__main__':
    generate_hosts = Generate_ansible_hosts('hosts')
    data = generate_hosts.read_host_file()
    print data
    # data = [
	 #    {
    #         "group": "dbservers",
    #         "items": [
    #             {
    #             "name": "oggsource",
    #             "ssh_host": "192.168.29.35",
    #             "ssh_port": 22,
    #             "ssh_user": "root",
    #             "ssh_password": "rootroot"
    #             },
    #             {
    #                 "name": "oggtarget",
    #                 "ssh_host": "192.168.29.37",
    #                 "ssh_port": 22,
    #                 "ssh_user": "root",
    #                 "ssh_password": "rootroot"
    #             },
    #             {
    #                 "name": "bindesktop",
    #                 "ssh_host": "192.168.29.28",
    #                 "ssh_port": 22,
    #                 "ssh_user": "root",
    #                 "ssh_password": "123abc,."
    #             }
    #         ]
	 #    }
    # ]
    generate_hosts.create_all_servers(data)