import jenkins

username = 'admin'
password = '2817f52c53c0e99f2c208ac761c1cee4'

server = jenkins.Jenkins('http://localhost:8080', username='admin', password='2817f52c53c0e99f2c208ac761c1cee4')

job_name = 'test'

param_dict = {'name1':'111','action_type':'rollback'}
print server.build_job(job_name,parameters=param_dict)
# param_dict = {}
# data = server.get_job_info(job_name)
# print data

# for var in  data['property'][0]['parameterDefinitions']:
#     param_dict[var['defaultParameterValue']['name']] = var['defaultParameterValue']['value']
#
# server.build_job(job_name,parameters=param_dict)

# print server.get_job_info(job_name)['lastBuild']['number']
# print server.get_job_info(job_name)
# server.get_job_info(job_name,depth=0)

# build_number = 5
# # print server.get_build_info(job_name,build_number)
# print server.get_build_info(job_name,build_number)

# print server.get_job_config(job_name)
# print server.get_build_info(job_name,5)
# print server.get_info()
# print server.get_all_jobs()

# print server.get_jobs()
# for job_name, job_instance in server.get_jobs():
#     print 'Job Name:%s' % (job_instance.name)
#     print 'Job Description:%s' % (job_instance.get_description())
#     print 'Is Job running:%s' % (job_instance.is_running())
#     print 'Is Job enabled:%s' % (job_instance.is_enabled())

# output = server.build_job(job_name)
# print output