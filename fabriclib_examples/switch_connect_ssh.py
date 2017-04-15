__author__ = 'Suhas Bharadwaj (subharad)'

# Import the fabric pkg
from fabriclib import Fabric


# have a list of switch ips that you are interested in
all_ips = ['10.126.94.105', '10.126.94.128']

# Create a fabric object(fab1) with a fabric name(say 'Bank1-fabric-A')
fab1 = Fabric('Bank1-fabric-A')

# Connect to all switches via ssh
# default username is 'admin' default password is 'nbv_12345', default connection type is 'ssh'
fab1.connect_to_switches_in_fabric(all_ips,password='nbv!2345')


# Get the switch objects after the connection,
# o/p is a dictionary of ip and swobj, ip is key and swobj is value
# Switch objects is an object of type 'Switch' defined under fabriclib pkg
all_sw_objs = fab1.get_all_sw_objs()


# You can then iterate and execute 'Switch' related methods
# for the switch objects (say get_swVersion, get_swHardwareType)
for ip in all_ips:
    print "\n---------------------------------------------------------"
    print "Switch ip is " + ip
    print "Switch sw version is " + all_sw_objs[ip].get_sw_version()
    print "Switch hw type is " + all_sw_objs[ip].get_sw_hardware_type()

    # You can even send cmd at different level, config_mode, exec_mode or under_module
    # Output is a list with all the lines of the cmd o/p
    output = all_sw_objs[ip].send_cmd_config_mode('show switchname')
    print "show switchname cmd o/p is : "
    print output



'''
OUPUT OF THE ABOVE CODE IS


---------------------------------------------------------
Switch ip is 10.126.94.105
Switch sw version is 8.1(1u)
Switch hw type is 9250i
show switchname cmd o/p is :
['show switchname\r\r', 'sw105-9250i\r', '\rsw105-9250i(config)#']

---------------------------------------------------------
Switch ip is 10.126.94.128
Switch sw version is 8.1(1)
Switch hw type is 9396S
show switchname cmd o/p is :
['show switchname\r\r', 'sw123456789\r', '\rsw123456789(config)#']



'''