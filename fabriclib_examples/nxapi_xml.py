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

print "\nSwitch version is : " + xmltodict.parse(op)['ins_api']['outputs']['output']['body']['sys_ver_str']
print "\nComplete XML output is as follows :-\n"
print op

# Lets configure the switch name
op = nxapi_sw.conf('conf t ; switchname sw123456789')
print "\ncommand output for setting switchname is  :-" + xmltodict.parse(op)['ins_api']['outputs']['output'][1]['msg']
print "\nComplete XML output is as follows :-" + op
