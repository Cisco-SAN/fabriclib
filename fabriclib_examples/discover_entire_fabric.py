__author__ = 'Suhas Bharadwaj (subharad)'

import logging.config

# Import Fabric and Switch class from fabriclib pkg
from fabriclib import Fabric

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': 'logfile_discover_entire_fabric.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'fabriclib': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'paramiko': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('fabriclib')
logger.info("Start of script...")

# Have a seed ip defined
seed_ip = '10.126.94.101'

# Create a fabric object with a fabric name
# fabric object 'f1' is of type Fabric class which is defined in fabriclib pkg
f1 = Fabric('Suhas TestBed - 1')

# Discover all the switches in the fabric by using the seed ip
# If the seed ip is an NPV switch then the 'discover_all_switches_in_fabric'
# method will o/p an error which can be caught and an exception can be thrown accordingly
print "Discovering the entire fabric. Please wait..."
f1.discover_all_switches_in_fabric(seed_ip, password='nbv!2345', discover_npv=False)

# Get the switch objects after the connection,
# o/p is a dictionary of ip and swobj, ip is key and swobj is value
# Switch objects is an object of type 'Switch' defined under fabriclib pkg
all_sw_objs = f1.get_all_sw_objs()

# You can then iterate and execute 'Switch' class related methods for the switch objects
# Note that in method 1 we iterated over the list of IPs given here we iterate over switch objects
for ip, swobj in all_sw_objs.iteritems():
    print "\n---------------------------------------------------------"
    print "Switch ip is " + ip
    print "Switch sw version is " + swobj.get_sw_version()
    print "Switch hw type is " + swobj.get_sw_hardware_type()



    # You can even send cmd at different level, config_mode, exec_mode or under_module
    # Output is a list with all the lines of the cmd o/p
    #output = swobj.send_cmd_config_mode('show switchname')
    #print "sh switchname cmd o/p is : "
    #print output

logger.info("End of script...")

















'''
OUTPUT OF THE ABOVE CODE IS AS BELOW

/Users/subharad/suenv/bin/python /Users/subharad/PycharmProjects/my-python-projects/fabriclib_examples/discover_entire_fabric.py
[23/Mar/2017 22:17:58] INFO Start of script...
INFO:fabriclib:Start of script...
[23/Mar/2017 22:17:58] INFO Attempting to connect to switch 10.126.94.101. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.101. Please wait...
Discovering the entire fabric. Please wait...
[23/Mar/2017 22:18:00] INFO Ssh to switch 10.126.94.101(sw101-9513) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.101(sw101-9513) was successful
[23/Mar/2017 22:18:00] INFO Attempting to connect to switch 10.126.94.103. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.103. Please wait...
[23/Mar/2017 22:18:00] INFO Attempting to connect to switch 10.126.94.102. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.102. Please wait...
[23/Mar/2017 22:18:00] INFO Attempting to connect to switch 10.126.94.108. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.108. Please wait...
[23/Mar/2017 22:18:00] INFO Attempting to connect to switch 10.126.94.110. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.110. Please wait...
[23/Mar/2017 22:18:02] INFO Ssh to switch 10.126.94.110(sw110-Mini) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.110(sw110-Mini) was successful
[23/Mar/2017 22:18:02] INFO Ssh to switch 10.126.94.103(sw103-9513) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.103(sw103-9513) was successful
[23/Mar/2017 22:18:02] INFO Ssh to switch 10.126.94.102(sw102-9509) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.102(sw102-9509) was successful
[23/Mar/2017 22:18:02] INFO Ssh to switch 10.126.94.108(sw108-9250i) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.108(sw108-9250i) was successful
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.109. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.109. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.129. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.129. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.128. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.128. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.107. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.107. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.106. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.106. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.105. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.105. Please wait...
[23/Mar/2017 22:18:03] INFO Attempting to connect to switch 10.126.94.104. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.104. Please wait...
[23/Mar/2017 22:18:03] INFO Ssh to switch 10.126.94.129(sw129-Luke) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.129(sw129-Luke) was successful
[23/Mar/2017 22:18:03] INFO Ssh to switch 10.126.94.104(sw104-Luke) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.104(sw104-Luke) was successful
[23/Mar/2017 22:18:06] INFO Ssh to switch 10.126.94.109(sw109-Mini) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.109(sw109-Mini) was successful
[23/Mar/2017 22:18:06] INFO Ssh to switch 10.126.94.128(sw123456789) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.128(sw123456789) was successful
[23/Mar/2017 22:18:06] INFO Ssh to switch 10.126.94.107(sw107-9250i) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.107(sw107-9250i) was successful
[23/Mar/2017 22:18:06] INFO Ssh to switch 10.126.94.105(sw105-9250i) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.105(sw105-9250i) was successful
[23/Mar/2017 22:18:07] INFO Ssh to switch 10.126.94.106(sw106-9250i) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.106(sw106-9250i) was successful
[23/Mar/2017 22:18:07] INFO Attempting to connect to switch 10.126.94.175. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.175. Please wait...
[23/Mar/2017 22:18:07] INFO Attempting to connect to switch 10.126.94.185. Please wait...
INFO:fabriclib.all_modules.switch:Attempting to connect to switch 10.126.94.185. Please wait...
[23/Mar/2017 22:18:07] INFO Ssh to switch 10.126.94.175(sw175-Luke-18slot) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.175(sw175-Luke-18slot) was successful
[23/Mar/2017 22:18:09] INFO Ssh to switch 10.126.94.185(sw185-9250i-2dot2) was successful
INFO:fabriclib.all_modules.switch:Ssh to switch 10.126.94.185(sw185-9250i-2dot2) was successful

---------------------------------------------------------
Switch ip is 10.126.94.109
Switch sw version is 8.1(1u)
Switch hw type is 9148S
sh switchname cmd o/p is :
['show switchname\r\r', 'sw109-Mini\r', '\rsw109-Mini(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.108
Switch sw version is 8.1(1)
Switch hw type is 9250i
sh switchname cmd o/p is :
['show switchname\r\r', 'sw108-9250i\r', '\rsw108-9250i(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.110
Switch sw version is 8.1(1u)
Switch hw type is 9148S
sh switchname cmd o/p is :
['show switchname\r\r', 'sw110-Mini\r', '\rsw110-Mini(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.128
Switch sw version is 8.1(1)
Switch hw type is 9396S
sh switchname cmd o/p is :
['show switchname\r\r', 'sw123456789\r', '\rsw123456789(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.175
Switch sw version is 8.1(1u)
Switch hw type is 9718
sh switchname cmd o/p is :
['show switchname\r\r', 'sw175-Luke-18slot\r', '\rsw175-Luke-18slot(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.103
Switch sw version is 7.3(1)DY(1)
Switch hw type is 9513
sh switchname cmd o/p is :
['show switchname\r\r', 'sw103-9513\r', '\rsw103-9513(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.102
Switch sw version is 7.3(1)DY(1)
Switch hw type is 9509
sh switchname cmd o/p is :
['show switchname\r\r', 'sw102-9509\r', '\rsw102-9509(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.101
Switch sw version is 7.3(1)DY(1)
Switch hw type is 9513
sh switchname cmd o/p is :
['show switchname\r\r', 'sw101-9513\r', '\rsw101-9513(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.107
Switch sw version is 8.1(1u)
Switch hw type is 9250i
sh switchname cmd o/p is :
['show switchname\r\r', 'sw107-9250i\r', '\rsw107-9250i(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.106
Switch sw version is 8.1(1u)
Switch hw type is 9250i
sh switchname cmd o/p is :
['show switchname\r\r', 'sw106-9250i\r', '\rsw106-9250i(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.105
Switch sw version is 8.1(1u)
Switch hw type is 9250i
sh switchname cmd o/p is :
['show switchname\r\r', 'sw105-9250i\r', '\rsw105-9250i(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.104
Switch sw version is 8.1(1u)
Switch hw type is 9710
sh switchname cmd o/p is :
['show switchname\r\r', 'sw104-Luke\r', '\rsw104-Luke(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.185
Switch sw version is 8.1(1u)
Switch hw type is 9250i
sh switchname cmd o/p is :
['show switchname\r\r', 'sw185-9250i-2dot2\r', '\rsw185-9250i-2dot2(config)# ']

---------------------------------------------------------
Switch ip is 10.126.94.129
Switch sw version is 8.1(1u)
Switch hw type is 9710
[23/Mar/2017 22:18:24] INFO End of script...
sh switchname cmd o/p is :
INFO:fabriclib:End of script...
['show switchname\r\r', 'sw129-Luke\r', '\rsw129-Luke(config)# ']
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.109 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.109 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.108 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.108 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.110 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.110 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.128 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.128 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.175 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.175 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.103 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.103 Ssh session is closed
[23/Mar/2017 22:18:24] INFO Session close:  Switch 10.126.94.102 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.102 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.101 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.101 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.107 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.107 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.106 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.106 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.105 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.105 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.104 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.104 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.185 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.185 Ssh session is closed
[23/Mar/2017 22:18:25] INFO Session close:  Switch 10.126.94.129 Ssh session is closed
INFO:fabriclib.all_modules.switch:Session close:  Switch 10.126.94.129 Ssh session is closed

Process finished with exit code 0





'''