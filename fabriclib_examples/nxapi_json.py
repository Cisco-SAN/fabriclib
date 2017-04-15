__author__ = 'Suhas Bharadwaj (subharad)'

# Import the fabric pkg
from fabriclib import Fabric

# Create a fabric object(f) with a fabric name(say 'Bank1-fabric-A')
f1 = Fabric('Bank1-fabric-A')

# Now lets connect to the switch via NXAPI url and switch credentials
nxapi_sw = f1.connect_to_nxapi_switch(ip_address='10.126.94.128',username='admin',password='nbv!2345',url='http://10.126.94.128:8081/')

# Set message format as 'json' and command type as 'cli_show', default message format is xml
nxapi_sw.setMsgFormat_and_CmdType(msg_fmt='json',cmd_type='cli_show')

# Lets get the o/p of 'show version' command
op = nxapi_sw.show('show version')
print "\nSwitch version is : " + op['ins_api']['outputs']['output']['body']['kickstart_ver_str']
print "\nComplete XML output is as follows :- "
print op

# Set message format as 'json' and command type as 'cli_conf', default message format is xml
nxapi_sw.setMsgFormat_and_CmdType(msg_fmt='json',cmd_type='cli_conf')

# Lets configure the switch name
op = nxapi_sw.conf('conf t ; switchname sw123456789')
print "\ncommand output for setting switchname is  :- " + op['ins_api']['outputs']['output'][1]['msg']
print "\nComplete XML output is as follows :-"
print op


'''
OUPUT OF THE ABOVE CODE IS

Switch version is : 8.1(1) [build 8.1(0.85)]

Complete XML output is as follows :-
{u'ins_api': {u'outputs': {u'output': {u'msg': u'Success', u'input': u'show version', u'code': u'200', u'body': {u'kern_uptm_secs': 21, u'kick_file_name': u'bootflash:///m9300-s1ek9-kickstart-mz.8.1.0.85.bin', u'rr_service': u'', u'loader_ver_str': u'N/A', u'module_id': u'2/4/8/10/16 Gbps FC/Supervisor-4', u'kick_tmstmp': u'03/21/2017 22:26:00', u'isan_file_name': u'bootflash:///m9300-s1ek9-mz.8.1.0.85.bin', u'sys_ver_str': u'8.1(1) [build 8.1(0.85)]', u'bootflash_size': 3915776, u'kickstart_ver_str': u'8.1(1) [build 8.1(0.85)]', u'kick_cmpl_time': u' 4/30/2017 23:00:00', u'chassis_id': u'MDS 9396S 96X16G FC (2 RU) Chassis', u'proc_board_id': u'JAE183600CQ', u'memory': 3890552, u'manufacturer': u'Cisco Systems, Inc.', u'kern_uptm_mins': 53, u'bios_ver_str': u'5.2.19', u'cpu_name': u'Motorola, 476fpe', u'bios_cmpl_time': u'05/15/2015', u'kern_uptm_hrs': 9, u'rr_usecs': 564169, u'isan_tmstmp': u'03/22/2017 00:01:06', u'rr_sys_ver': u'8.1(0.65)', u'rr_reason': u'Reset Requested by CLI command reload', u'rr_ctime': u' Thu Mar 23 04:42:47 2017\n', u'header_str': u'Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\nCopyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.\nThe copyrights to certain works contained herein are owned by\nother third parties and are used and distributed under license.\nSome parts of this software are covered under the GNU Public\nLicense. A copy of the license is available at\nhttp://www.gnu.org/licenses/gpl.html.\n', u'isan_cmpl_time': u' 4/30/2017 23:00:00', u'host_name': u'sw123456789', u'mem_type': u'kB', u'kern_uptm_days': 0}}}, u'version': u'1.2', u'type': u'cli_show', u'sid': u'eoc'}}

command output for setting switchname is  :- Success

Complete XML output is as follows :-
{u'ins_api': {u'outputs': {u'output': [{u'msg': u'Success', u'input': u'conf t', u'code': u'200', u'body': {}}, {u'msg': u'Success', u'input': u' switchname sw123456789', u'code': u'200', u'body': {}}]}, u'version': u'1.2', u'type': u'cli_conf', u'sid': u'eoc'}}


'''
