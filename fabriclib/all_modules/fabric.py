__author__ = 'Suhas Bharadwaj (subharad)'

import ConfigParser
import logging
import os
import threading
from functools import wraps
logging.basicConfig()
from .switch import Switch
from .nxapi_switch import Nxapi_Switch
logger = logging.getLogger(__name__)


def wait_till_connect_threads_complete(fn):
    """
    Decorator which will check if all the 'connect' method's threads are complete by doing a join
    :param fn: Function that needs to be decorated.
    This function 'fn' is called and after which we wait till all the child threads with the name 'connect' are finished
    :return: None
    """

    @wraps(fn)
    def th_complete(*a, **kw):
        # Call the function which was decorated mostly it will be the 'connect' method of 'Switch' class
        ret = fn(*a, **kw)
        # Wait till all 'connect' threads are complete
        for t in threading.enumerate():
            # print t.getName()
            if t.getName() == 'connect':
                t.join()
        return ret

    return th_complete

class Fabric(object):
    """

    """

    def __init__(self, fabric_name="New_Fabric"):
        """

        :param fabric_name:
        :return:
        """

        # Fabric name
        self.__fab_name = fabric_name

        # Switch related variables
        self.__fab_seed_sw_ip = ""
        self.__fab_swuser = ""
        self.__fab_swpassword = ""
        self.__fab_swconntype = ""
        self.__fab_sw_obj_dict = {}

    def discover_all_switches_in_fabric(self, seed_ip, username='admin', password='nbv_12345', conntype='ssh',
                                        discover_npv=True):
        """

        :param seed_ip:
        :param username:
        :param password:
        :param conntype:
        :param discover_npv:
        :return:
        """

        error = False
        errorDetails = "None"

        if conntype != 'ssh' and conntype != 'telnet':
            errorDetails = "Conntype argument has to be 'ssh' or 'telnet', for nxapi use the method 'connect_to_nxapi_switch' "
            logger.error(errorDetails)
            return [error, errorDetails]

        self.__fab_seed_sw_ip = seed_ip
        ips_to_be_discovered = [seed_ip]

        while ips_to_be_discovered.__len__() != 0:

            self.__connect_to_all_dut_switches(ips_to_be_discovered, username, password, conntype)

            if self.__fab_sw_obj_dict[seed_ip].is_switch_in_NPV_mode():
                error = True
                errorDetails = "Switch ip " + seed_ip + " is an NPV switch, you cannot use NPV switch as seed switch"
                logger.error(errorDetails)
                return [error, errorDetails]
            else:
                self.__execute_sh_topo(ips_to_be_discovered)
                if discover_npv:
                    self.__execute_sh_fcns_da_detail(ips_to_be_discovered)

                peer_ip_list = []
                for ip in ips_to_be_discovered:
                    peer_ip_list.extend(self.__fab_sw_obj_dict[ip].get_peer_ip_list())
                    if discover_npv:
                        peer_ip_list.extend(self.__fab_sw_obj_dict[ip].get_peer_npv_ip_list())
                ips_to_be_discovered = set(peer_ip_list)
                for ip in self.__fab_sw_obj_dict.keys():
                    if ip in ips_to_be_discovered:
                        ips_to_be_discovered.remove(ip)

        return [error, errorDetails]

    def connect_to_switches_in_fabric(self, fabric_switch_ip_list, username='admin', password='nbv_12345',
                                      conntype='ssh'):
        """

        :param fabric_switch_ip_list:
        :param username:
        :param password:
        :param conntype:
        :return:
        """

        error = False
        errorDetails = "None"

        self.__connect_to_all_dut_switches(fabric_switch_ip_list, username, password, conntype)

        return [error, errorDetails]

    def connect_to_nxapi_switch(self,ip_address, username='admin', password='nbv_12345', url = ''):
        """

        :param ip_address:
        :param username:
        :param password:
        :param url:
        :return:
        """
        self.__fab_swuser = username
        self.__fab_swpassword = password
        self.__fab_swconntype = 'nxapi'
        nxapi_sw = Nxapi_Switch(ip_address,username,password,url)
        self.__fab_sw_obj_dict[ip_address] = nxapi_sw

        return self.__fab_sw_obj_dict[ip_address]

    @wait_till_connect_threads_complete
    def __execute_sh_topo(self, swip_swobj_dict):
        """

        :param swip_swobj_dict:
        :return:
        """
        for ip in swip_swobj_dict:
            self.__fab_sw_obj_dict[ip].execute_sh_topo_cmd()
        # print("ece")
        return ""

    @wait_till_connect_threads_complete
    def __execute_sh_fcns_da_detail(self, swip_swobj_dict):
        """

        :param swip_swobj_dict:
        :return:
        """
        for ip in swip_swobj_dict:
            self.__fab_sw_obj_dict[ip].execute_sh_fcns_da_detail_cmd()
        # print("sh fc")
        return ""

    @wait_till_connect_threads_complete
    def __execute_sh_int_brief_and_sh_zs_active_cmd(self):
        """

        :return:
        """
        for ip in self.__fab_sw_obj_dict.keys():
            self.__fab_sw_obj_dict[ip].execute_sh_int_brief_and_sh_zs_active_cmd()
        # print("sh fc")
        return ""

    @wait_till_connect_threads_complete
    def __connect_to_all_dut_switches(self, fabric_switch_ip_list, username, password, conntype):
        """
         Creates a switch object with each ip in self.__fab_switch_ip_list
        Then connects to the siwtch by calling the switch's 'connect' method
        Since switch's 'connect' method runs in a thread, we call the decorator
        'wait_till_connect_threads_complete' to make sure all threads are complete, that means
        all switches were connected successfully
        :param fabric_switch_ip_list:
        :param username:
        :param password:
        :param conntype:
        :return: None
        """

        self.__fab_swuser = username
        self.__fab_swpassword = password
        self.__fab_swconntype = conntype

        for ip in fabric_switch_ip_list:
            # Create Switch object
            s = Switch(ip, self.__fab_swuser, self.__fab_swpassword, self.__fab_swconntype)
            # Append that switch object to a list
            self.__fab_sw_obj_dict[ip] = s
            # Connect to that switch
            s.connect()

        return self.get_all_sw_objs()

    def get_fabric_name(self):
        """

        :return:
        """
        return self.__fab_name

    def get_all_sw_objs(self):
        """
        Return the list of all switch objects
        :return: self.__fab_sw_obj_dict
        """
        return self.__fab_sw_obj_dict

    def get_all_sw_ip_addrs(self):
        """

        :return:
        """
        return sorted(self.__fab_sw_obj_dict.keys())
