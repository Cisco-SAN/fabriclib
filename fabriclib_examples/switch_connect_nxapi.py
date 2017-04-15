__author__ = 'Suhas Bharadwaj (subharad)'
import xmltodict

# Import the fabric pkg
from fabriclib import Fabric

# Create a fabric object(f) with a fabric name(say 'Bank1-fabric-A')
f1 = Fabric('Bank1-fabric-A')

# Now lets connect to the switch via NXAPI url and switch credentials
nxapi_sw = f1.connect_to_nxapi_switch(ip_address='10.126.94.128',username='admin',password='nbv!2345',url='http://10.126.94.128:8081/')

# Lets get the o/p of 'show version' command
op = nxapi_sw.show('show version')

print "\nSwitch version is : " + xmltodict.parse(op)['ins_api']['outputs']['output']['body']['kickstart_ver_str']
print "\nComplete XML output is as follows :-"
print op



'''
OUPUT OF THE ABOVE CODE IS

Switch version is : 8.1(1) [build 8.1(0.85)]

Complete XML output is as follows :-
<?xml version="1.0"?>
<ins_api>
  <type>cli_show</type>
  <version>1.2</version>
  <sid>eoc</sid>
  <outputs>
    <output>
      <body>
      <header_str>Cisco Nexus Operating System (NX-OS) Software
TAC support: http://www.cisco.com/tac
Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
Copyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.
The copyrights to certain works contained herein are owned by
other third parties and are used and distributed under license.
Some parts of this software are covered under the GNU Public
License. A copy of the license is available at
http://www.gnu.org/licenses/gpl.html.
</header_str>
      <bios_ver_str>5.2.19</bios_ver_str>
      <loader_ver_str>N/A</loader_ver_str>
      <kickstart_ver_str>8.1(1) [build 8.1(0.85)]</kickstart_ver_str>
      <sys_ver_str>8.1(1) [build 8.1(0.85)]</sys_ver_str>
      <bios_cmpl_time>05/15/2015</bios_cmpl_time>
      <kick_file_name>bootflash:///m9300-s1ek9-kickstart-mz.8.1.0.85.bin</kick_file_name>
      <kick_cmpl_time> 4/30/2017 23:00:00</kick_cmpl_time>
      <kick_tmstmp>03/21/2017 22:26:00</kick_tmstmp>
      <isan_file_name>bootflash:///m9300-s1ek9-mz.8.1.0.85.bin</isan_file_name>
      <isan_cmpl_time> 4/30/2017 23:00:00</isan_cmpl_time>
      <isan_tmstmp>03/22/2017 00:01:06</isan_tmstmp>
      <chassis_id>MDS 9396S 96X16G FC (2 RU) Chassis</chassis_id>
      <module_id>2/4/8/10/16 Gbps FC/Supervisor-4</module_id>
      <cpu_name>Motorola, 476fpe</cpu_name>
      <memory>3890552</memory>
      <mem_type>kB</mem_type>
      <proc_board_id>JAE183600CQ</proc_board_id>
      <host_name>sw123456789</host_name>
      <bootflash_size>3915776</bootflash_size>
      <kern_uptm_days>0</kern_uptm_days>
      <kern_uptm_hrs>9</kern_uptm_hrs>
      <kern_uptm_mins>36</kern_uptm_mins>
      <kern_uptm_secs>40</kern_uptm_secs>
      <rr_usecs>564169</rr_usecs>
      <rr_ctime> Thu Mar 23 04:42:47 2017
</rr_ctime>
      <rr_reason>Reset Requested by CLI command reload</rr_reason>
      <rr_sys_ver>8.1(0.65)</rr_sys_ver>
      <rr_service/>
      <manufacturer>Cisco Systems, Inc.</manufacturer>
     </body>
      <input>show version</input>
      <msg>Success</msg>
      <code>200</code>
    </output>
  </outputs>
</ins_api>

'''
