__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import re
import socket
import telnetlib
import threading
import time
import traceback
from functools import wraps
logging.basicConfig()
import paramiko

from fabriclib.all_parsers import ShowTopology, ShowFcnsDatabaseDetail, ShowInterfaceBrief, ShowPortChannelDatabase

logger = logging.getLogger(__name__)


def run_in_background(fn):
    """

    doc string of run_in_background
    Decorator used to run the 'Switch' class' 'connect' method in a thread with thread name as 'connect'
    Also note that this decorator just creates the thread and starts the thread
    In case you need to check if threads are finished, pls check the decorator
    'wait_till_connect_threads_complete' written in 'Fabric' class

    :param fn: Function which needs to be run in a thread
    :return: None
    """

    @wraps(fn)
    def start_thread(*a, **kw):
        """
        doc string of start_thread
        actual wrapper which starts a thread
        :param a:
        :param kw:
        :return:
        """
        t = threading.Thread(name="connect", target=fn, args=a, kwargs=kw)
        # print t.getName()
        t.start()
        # return t # return the thread id so that we can use join to wait for completion

    return start_thread

def log_as_debug(fn, logaslevelinfo=False):
    @wraps(fn)
    def log_debug(*args, **kwargs):
        val = fn(*args, **kwargs)
        for i in val:
            if logaslevelinfo:
                logger.info(str(i).strip('\n\r'))
            else:
                logger.debug("send_cmd  " + str(i).strip('\n\r'))
        return val

    return log_debug

class Switch(object):
    """
    The is a switch connection class which takes switch ip,username and password
    and provide a switch connection object
    """

    def __init__(self, ip_address, username='admin', password='nbv_12345', conntype='ssh'):

        self.__timeout_value = 30

        self.__swipaddrs = ip_address
        self.__swuser = username
        self.__swpassword = password
        self.__swconntype = conntype
        self.__swconnobj = ""
        self.__shell = ""
        self.__swname = ""

        self.__sw_peer_ip_list = []
        self.__sw_peer_npv_ip_list = []

        # All the 'up/trunking' ports and port mode details on the switch are stored as string
        # Details are got from 'sh int brif | i fc' cmd
        # this is req for populating checkboxes
        # Sample : fc1/25 TE fc1/26 F fc1/27 TE fc4/3 TE fc4/4 TE fc4/13 TE
        self.__sw_all_up_ports = ""

        # All the local active zoneset's fcids are stored as list
        # Details got from 'sh zoneset active | grep *' cmd
        # Sample : ['0x3f012a', '0x3f012b', '0x3f012c', '0x3f012d']
        self.__sw_all_local_active_zs_fcids = []

        # If any of the local port is part of active zoneset's database in the entire fabric
        # then those port details are stored here
        # this is req for populating checkboxes
        # Sample : fc1/26 F fc4/13 F
        self.__sw_local_port_details_active_zs = []

        self.__connected_links = []

        self.__connected_endports = []

    @run_in_background
    def connect(self):
        """

        connects to the switch via telnet or ssh which ever option was passed while
        creating the class object
        decorator 'run_in_background' is called to run this connect in a thread

        :return: None
        """

        # print "INside connect"
        logger.info("Attempting to connect to switch %s. Please wait..." % self.__swipaddrs)
        logger.debug("ip:%s username:%s password:%s" % (self.__swipaddrs, self.__swuser, self.__swpassword))
        if self.__swconntype == "ssh":
            try:
                logger.debug("inside ssh")
                self.__swconnobj = paramiko.SSHClient()
                self.__swconnobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.__swconnobj.connect(self.__swipaddrs, username=self.__swuser, password=self.__swpassword,
                                         timeout=self.__timeout_value)
                self.__shell = self.__swconnobj.invoke_shell()
                self.__shell.settimeout(self.__timeout_value)
                a = self.__process_cmd("terminal len 0", True)

                a = self.__process_cmd("show switchname")
                self.__swname = a.split("\n")[1].strip("\r")
                logger.info(
                    self.__swconntype.title() + " to switch " + self.__swipaddrs + "(" + self.__swname + ") was successful")

            except paramiko.AuthenticationException:
                logger.critical("Authentication failed when connecting to %s" % self.__swipaddrs)
                exit()

            except paramiko.BadHostKeyException:
                logger.critical("Bad host ip exception")
                exit()
            except paramiko.ChannelException:
                logger.critical("Channel  exception")
                exit()
            except paramiko.SSHException:
                logger.critical("Could not SSH to %s, waiting for it to start" % self.__swipaddrs)
                exit()

            except Exception, err:
                print(traceback.format_exc())
                logger.critical(traceback.format_exc())
                logger.critical(
                    "unable to ssh to the switch %s ,Pls check if ssh is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()

        elif self.__swconntype == "telnet":
            try:
                logger.debug("inside telnet")
                # Set debug level as 1 to enable telnet debugging
                telnetdebug = 0
                self.__swconnobj = telnetlib.Telnet(self.__swipaddrs, timeout=self.__timeout_value)
                self.__swconnobj.set_debuglevel(telnetdebug)
                self.__swconnobj.read_until("login:", timeout=self.__timeout_value)
                b = str(self.__swuser + "\n")
                self.__swconnobj.write(b)
                self.__swconnobj.read_until("Password:", timeout=self.__timeout_value)
                b = str(self.__swpassword + "\n")
                self.__swconnobj.write(b)
                self.__swconnobj.read_until("#", timeout=self.__timeout_value)
                self.__swconnobj.write("\n")
                self.__swconnobj.read_until("#", timeout=self.__timeout_value)
                self.__swconnobj.write("\n")
                self.__swconnobj.read_until("#", timeout=self.__timeout_value)
                self.__swconnobj.write("terminal length 0\n")
                self.__swconnobj.read_until("#", timeout=self.__timeout_value)
                self.__swconnobj.write("\n")
                out = self.__swconnobj.read_until("#", timeout=self.__timeout_value)
                self.__swname = ''.join(out.split()).strip("#")
                logger.info(
                    self.__swconntype.title() + " to switch " + self.__swipaddrs + "(" + self.__swname + ") was successful")

            except EOFError:
                logger.critical("hit EOFError while trying to connect to switch with ip %s", self.__swipaddrs)
                exit()
            except socket.timeout:
                logger.critical(
                    "Socket time out: Unable to telnet to the switch %s ,Pls check if telnet is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()
            except Exception, err:
                print(traceback.format_exc())
                logger.critical(traceback.format_exc())
                logger.critical(
                    "unable to telnet to the switch %s ,Pls check if telnet is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()

    @log_as_debug
    def send_cmd(self, cmd, wait_till_prompt="#"):

        """
        switchcmd method runs non-blocking commands provided as an argument
        :parameter cmd: Takes switch command string as a parameter
        :return: the command output
        """
        logger.debug("Attempting to execute the cmd '" + cmd + "' on switch " + self.__swipaddrs)
        if self.__swconntype == 'ssh':
            try:
                returnoutput = self.__process_cmd(cmd, prompt=wait_till_prompt)
                return returnoutput.split("\n")

            except paramiko.AuthenticationException:
                logger.critical(self.__swipaddrs + ": Authentication failed when send cmd to %s" % self.__swipaddrs)
                exit()

            except paramiko.BadHostKeyException:
                logger.critical(self.__swipaddrs + ": Bad host ip exception")
                exit()
            except paramiko.ChannelException:
                logger.critical(self.__swipaddrs + ": Channel  exception")
                exit()
            except paramiko.SSHException:
                logger.critical(self.__swipaddrs + ": Could not SSH to %s, waiting for it to start" % self.__swipaddrs)
                exit()

            except Exception, err:
                print(traceback.format_exc())
                logger.critical(traceback.format_exc())
                logger.critical(
                    "unable to send cmds via ssh session to the switch %s ,Pls check if ssh is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()

        else:
            try:
                b = str(cmd + "\r\n")
                self.__swconnobj.write(b)
                output = self.__swconnobj.read_until(wait_till_prompt)
                return output.strip().strip("\r").split("\n")

            except EOFError:
                logger.critical(self.__swipaddrs + "hit EOFError while trying to connect to switch with ip %s",
                                self.__swipaddrs)
                exit()
            except socket.timeout:
                logger.critical(
                    "Socket time out: Unable to send cmd via telnet to the switch %s ,Pls check if telnet is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()
            except Exception, err:
                print(traceback.format_exc())
                logger.critical(traceback.format_exc())
                logger.critical(
                    "unable to send cmds via telnet to the switch %s ,Pls check if telnet is enabled on the switch and is reachable via this machine",
                    self.__swipaddrs)
                exit()

    def send_cmd_exec_mode(self, cmd):
        """

        :param cmd:
        :return:
        """
        self.send_cmd("end")
        return self.send_cmd(cmd)

    def send_cmd_config_mode(self, cmd):
        """

        :param cmd:
        :return:
        """
        self.send_cmd("end")
        self.send_cmd("conf t")
        return self.send_cmd(cmd)

    def send_cmd_under_module(self, mod, cmd):
        """

        :param mod:
        :param cmd:
        :return:
        """
        self.send_cmd("end")
        self.send_cmd("attach mod " + str(mod))
        self.send_cmd("terminal width 300")
        retval = self.send_cmd(cmd)
        self.send_cmd("exit")
        return retval

    def __process_cmd(self, command, chkPrompt=False, prompt="#"):
        """

        :param command:
        :param chkPrompt:
        :param prompt:
        :return:
        """

        stdout_data = ""

        try:
            if chkPrompt:
                # self.logger.info("Checking for prompt in buffer output")
                a = self.__shell.recv(1024)
                if "and wish to continue" in a:
                    self.__shell.send("\n")
                while not prompt in a:
                    a = self.__shell.recv(1024)
                    if "and wish to continue" in a:
                        self.__shell.send("\n")
            # self.logger.info("Executing cmd "+command)

            # Send the su command
            self.__shell.send(command + "\n")

            a = self.__shell.recv(1024)
            stdout_data += a
            # self.logger.debug("__shell rcv :"+a)

            while not prompt in a:
                a = self.__shell.recv(1024)
                a.strip("")
                stdout_data += a
                # self.logger.debug("__shell rcv :"+a)
                # self.logger.info("DONE with "+command)
        except socket.timeout:
            logger.critical(
                "Socket time out: Unable to send cmd via ssh  to the switch %s ,Pls check if ssh is enabled on the switch and is reachable via this machine",
                self.__swipaddrs)
            exit()

        return stdout_data

    def get_swusername_password(self):
        """

        :return:
        """
        return self.__swuser, self.__swpassword

    def get_ipaddress(self):
        """

        :return:
        """
        return self.__swipaddrs

    def get_conn_type(self):
        """

        :return:
        """
        return self.__swconntype

    def get_switchname(self):
        """

        :return:
        """
        return self.__swname

    def get_sw_version(self):
        """

        :return:
        """
        logger.debug("Getting the sw version of the switch " + self.get_ipaddress())
        cmd = "show version"
        pat = ".*system:    version (\S+)\s+"
        lines = self.send_cmd(cmd)
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                return matchObj.group(1)
        return "ERROR!! SW_VERSION NOT FOUND"

    def get_sw_hardware_type(self):
        """

        :return:
        """
        logger.debug("Getting the switch hardware type of the switch " + self.get_ipaddress())
        cmd = "show version"
        pat = ".*cisco MDS (\S+)\s+"
        lines = self.send_cmd(cmd)
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                return matchObj.group(1)
        return "ERROR!! SW_TYPE NOT FOUND"

    def get_mod_num_type_status(self,mod = ""):
        """

        :param mod:
        :return:
        """
        if mod == "":
            logger.debug("Getting all modules number,type and status " + self.get_ipaddress())
            cmd = "show mod"
        else:
            logger.debug("Getting all modules number,type and status " + self.get_ipaddress())
            cmd = "show mod " + str(mod)
        pat = "([0-9+]).*(DS\S+)\s+(\S+)"
        lines = self.send_cmd(cmd)
        allmods = []
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                a = (matchObj.group(1), matchObj.group(2), matchObj.group(3))
                allmods.append(a)
        if allmods.__len__() == 0:
            #The first paramenter '1' represents that an error occured and the next element describes the error
            #In future this can be modified based on the error thrown by cli
            return [1,"ERROR!! MOD DETAILS NOT FOUND"]
        else:
            # The first paramenter '0' represents that there was no error
            return [0,allmods]

    def get_mod_status(self,mod):
        """

        :param mod:
        :return:
        """
        logger.debug("Getting module status for module: " + str(mod))
        modstatus = self.get_mod_num_type_status(mod)
        if modstatus[0] != 0:
            logger.debug("Module status for module: " + str(mod) + " returned error, so sleeping for 10 secs and checking again..")
            time.sleep(10)
            modstatus = self.get_mod_num_type_status(mod)
            if modstatus[0] != 0:
                logger.debug("Module status for module: " + str(mod) + " returned error")
                logger.debug(modstatus)
                return "Error"
            else:
                return modstatus[1][0][2]
        else:
            return modstatus[1][0][2]


    def get_peer_ip_list(self):
        """

        :return:
        """
        return self.__sw_peer_ip_list

    def get_peer_npv_ip_list(self):
        """

        :return:
        """
        return self.__sw_peer_npv_ip_list

    def get_all_vsans(self):
        """

        :return:
        """
        logger.debug("Getting all vsans present on the switch " + self.get_ipaddress())
        cmd = "sh vsan  | i information"
        pat = "vsan\s+([0-9]+)\s+information"
        lines = self.send_cmd(cmd)
        vsanlist = []
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                vsanlist.append(matchObj.group(1))
        if vsanlist.__len__() == 0:
            return "ERROR!! VSAN list NOT FOUND"
        else:
            return tuple(vsanlist)

    def get_current_switch_time(self):
        """

        :return:
        """
        logger.debug("Getting current switch time on the switch " + self.get_ipaddress())
        cmd = "sh clock"
        pat = "(\d+:\d+\d+.*)"
        lines = self.send_cmd(cmd)
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                return (matchObj.group(1)).strip(' \t\n\r')
        logger.debug("ERROR!! SH CLOCK CMD DIDNT WORK")
        logger.debug("sh clk op is")
        logger.debug(lines)
        return "ERROR!! SH CLOCK CMD DIDNT WORK"

    def get_all_up_ports(self):
        """
        Returns all the up ports in this switch
        :return: __sw_all_up_ports
        """
        return self.__sw_all_up_ports

    def get_all_local_active_zs_fcids(self):
        """
        Returns all the active zoneset's fcids in the switch
        :return: __sw_all_local_active_zs_fcids
        """
        return self.__sw_all_local_active_zs_fcids

    def get_local_port_details_active_zs(self):
        """
        Returns all the up ports details in this switch which are present in active zoneset's database in the entire fabric
        :return: __sw_active_zs_up_ports
        """
        a = ""
        for t in self.__sw_local_port_details_active_zs:
            a = a + " ".join(t) + " "
        return a

    def get_connected_links(self):
        """

        :return:
        """
        return self.__connected_links

    def get_connected_endports(self):
        """

        :return:
        """
        return self.__connected_endports

    def set_local_port_mode_of_active_zs_fcid(self, fcidlist):
        """

        :param fcidlist:
        :return:
        """
        for fcid in fcidlist:
            port = self.__sh_fcns_da.get_local_port_and_mode_by_fcid(self.get_ipaddress(), fcid)
            pat = "^fc"
            if port != "" and re.match(pat, port):
                if port.__contains__('port-channel'):
                    cmd = "sh port-channel database"
                    li = self.sendcmd(cmd)
                    self.__sh_port_ch_data = ShowPortChannelDatabase(li)
                    plist = self.__sh_port_ch_data.get_pc_ports(port)
                    for p in plist:
                        i = self.get_all_up_ports().split().index(p[0])
                        m = self.get_all_up_ports().split()[(i + 1)]
                        self.__sw_local_port_details_active_zs.append([p[0], m])
                else:
                    i = self.get_all_up_ports().split().index(port)
                    m = self.get_all_up_ports().split()[(i + 1)]
                    self.__sw_local_port_details_active_zs.append([port, m])
        self.__sw_local_port_details_active_zs = [list(x) for x in
                                                  set(tuple(x) for x in self.__sw_local_port_details_active_zs)]

    @run_in_background
    def execute_sh_topo_cmd(self):
        """

        :return:
        """
        logger.debug("Getting all the peer ip list bu executing the sh topo cmd on switch" + self.get_ipaddress())
        cmd = "show topology"
        li = self.send_cmd_exec_mode(cmd)
        sh = ShowTopology(li)
        self.__sw_peer_ip_list = sh.get_all_peer_ip_addrs()
        self.__connected_links = sh.get_connected_links()

    @run_in_background
    def execute_sh_fcns_da_detail_cmd(self):
        """

        :return:
        """
        logger.debug("Executing 'sh fcns data detail' to get all flogi info for ip: " + self.get_ipaddress())
        cmd = "sh fcns data detail"
        li = self.send_cmd_exec_mode(cmd)
        self.__sh_fcns_da = ShowFcnsDatabaseDetail(li)

        # Set peer npv ip list
        self.__sw_peer_npv_ip_list = self.__sh_fcns_da.get_nodeip_if_fc4_is_NPV()

        self.__connected_endports = self.__sh_fcns_da.get_connected_endports(self.get_ipaddress())

    @run_in_background
    def execute_sh_int_brief_and_sh_zs_active_cmd(self):
        """

        :return:
        """
        logger.debug("Executing 'sh int br' to get all fc up ports for ip: " + self.get_ipaddress())
        li = self.send_cmd_exec_mode("sh interface brief | i ^fc")
        # print("Executing 'sh int br' to get all fc up ports for ip: " + self.get_ipaddress(),li)
        sh = ShowInterfaceBrief(li)
        a = sh.getFC_PortandOperModeasString()
        self.__sw_all_up_ports = a
        # print a

        logger.debug("Executing 'sh zoneset active' to get all fcids on switch: " + self.get_ipaddress())

        lines = self.send_cmd_exec_mode("sh zoneset active | grep *")
        for line in lines:
            # print line
            pat = ".*fcid (0x[0-9a-f]+) \[.*"
            matchobj = re.match(pat, line)
            if matchobj:
                self.__sw_all_local_active_zs_fcids.append(matchobj.group(1))

    def conf_vsan(self, vsan_num):
        """

        :param vsan_num:
        :return:
        """
        logger.debug("Configuring vsan " + vsan_num + " on the switch " + self.get_ipaddress())
        self.send_cmd_config_mode("vsan database")
        self.send_cmd("vsan " + vsan_num)

    def conf_port(self, port, ratemode='shared', mode='auto', speed='auto', shut_noshut='no shut'):
        """

        :param port:
        :param ratemode:
        :param mode:
        :param speed:
        :param shut_noshut:
        :return:
        """
        logger.debug(
            "Configuring port " + port + " on the switch " + self.get_ipaddress() + " to the following details")
        logger.debug(
            "rate-mode: " + ratemode + "; mode: " + mode + "; speed: " + speed + "; shut_noshut: " + shut_noshut)

        self.send_cmd_config_mode("int " + port)
        self.send_cmd("switchport rate-mode " + ratemode)
        self.send_cmd("switchport mode " + mode)
        self.send_cmd("switchport speed " + speed)
        self.send_cmd(shut_noshut)

    def conf_port_shutdown(self, port):
        """

        :param port:
        :return:
        """
        logger.debug("Shutting down the port " + port + " on the switch " + self.get_ipaddress())
        self.send_cmd_config_mode("int " + port)
        self.send_cmd("shutdown")

    def conf_port_no_shutdown(self, port):
        """

        :param port:
        :return:
        """
        logger.debug("No Shutting down the port " + port + " on the switch " + self.get_ipaddress())
        self.send_cmd_config_mode("int " + port)
        self.send_cmd("no shutdown")

    def conf_port_vsan(self, port, vsan_num):
        """

        :param port:
        :param vsan_num:
        :return:
        """
        logger.debug("Setting the " + port + " on the switch " + self.get_ipaddress() + " to vsan " + vsan_num)
        self.send_cmd_config_mode("vsan database")
        self.send_cmd("vsan " + vsan_num)
        self.send_cmd("vsan " + vsan_num + " intface " + port, wait_till_prompt=':')
        self.send_cmd("y")

    def is_switch_in_NPV_mode(self):
        """

        :return:
        """
        logger.debug("Finding if switch is an NPV switch for ip: " + self.get_ipaddress())
        cmd = "sh feature | i npv"
        pat = ".*enabled.*"
        lines = self.send_cmd(cmd)
        for line in lines:
            matchObj = re.match(pat, line)
            if matchObj:
                return True
        return False

    def execute_cmds_in_loop(self, cmdlist, count=1, delay=5, printonscreen=False, wait_till_prompt="#"):
        """

        :param cmdlist:
        :param count:
        :param delay:
        :param printonscreen:
        :param wait_till_prompt:
        :return:
        """
        s = "Executing the below cmdlist in a loop for " + str(count) + " times with a delay of " + str(
            delay) + " secs each on switch " + str(self.get_ipaddress())
        logger.debug(s)
        logger.debug(cmdlist)
        print s
        print cmdlist
        for i in range(0, count):
            for cmd in cmdlist:
                s = "######### Iteration : " + str(i + 1) + " ;  cmd : '" + str(cmd) + "' #########"
                logger.debug(s)
                if printonscreen:
                    print s
                out = self.send_cmd(cmd, wait_till_prompt=wait_till_prompt)

                for o in out:
                    s = "\t" + o.strip('\n\r')
                    logger.debug(s)
                    if printonscreen:
                        print s

                self.__sleep(delay, printonscreen)

    def flap_port(self, ports, count=1, delay=30):
        """

        :param ports:
        :param count:
        :param delay:
        :return:
        """
        s = "Flapping the ports " + ports + " " + str(count) + " times with a delay of " + str(
            delay) + " secs on switch " + str(self.get_ipaddress()) + " Please wait..."
        logger.debug(s)
        print s
        for i in range(0, count):
            s = "######### Flap iteration : " + str(i + 1) + " #########"
            logger.debug(s)
            self.send_cmd_config_mode("int " + ports)
            logger.debug("Shutting the port")
            self.send_cmd("shut")
            self.__sleep(delay)
            logger.debug("No Shutting the port")
            self.send_cmd("no shut")
            self.__sleep(delay)

    def check_cores(self):
        """

        :return:
        """
        coreFound = False
        lines = self.sendcmd("show cores")
        corelist = []
        for l in lines:
            if l.__contains__(":"):
                coreFound = True
                corelist.append(' '.join(l.split()))
                logger.critical("Core files found on switch : %s, Core file is (%s)", self.__swipaddrs,
                                ' '.join(l.split()))
        if coreFound:
            return corelist
        else:
            return "No core found"

    def __sleep(self, delay, printonscreen=False):
        """

        :param delay:
        :param printonscreen:
        :return:
        """
        s = "Sleeping for " + str(delay) + " seconds...."
        logger.debug(s)
        if printonscreen:
            print s
        time.sleep(delay)

    def __del__(self):
        """

        :return:
        """
        logger.info(
            "Session close:  Switch " + self.__swipaddrs + " " + self.__swconntype.title() + " session is closed")
        self.__swconnobj.close()
