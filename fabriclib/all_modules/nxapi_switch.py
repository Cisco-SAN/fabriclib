__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import requests
import json
import re
import socket
import telnetlib
import threading
import time
import traceback
from functools import wraps
logging.basicConfig()
import paramiko

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

class Nxapi_Switch(object):

    """
    The is a switch connection class which is used to discover switch via nxapi
    """

    def __init__(self, ip_address, username='admin', password='nbv_12345', url=''):
        """

        :param ip_address:
        :param username:
        :param password:
        :param url:
        """
        self.__timeout_value = 30

        self.__swipaddrs = ip_address
        self.__swuser = username
        self.__swpassword = password

        if url == '':
            url = "http://"+ self.__swipaddrs + "/ins"
        else:
            if url.endswith("/ins"):
                self.__url = url
            elif url.endswith("/"):
                self.__url = url + "ins"
            else:
                self.__url = url + "/ins"

        self.__msg_format = "xml"
        self.__cmd_type = "cli_show"

        self.__logInfoAbout_Url_MsgFmt_CmdType()


    def __logInfoAbout_Url_MsgFmt_CmdType(self):
        """

        :return:
        """
        logger.info("url is :" + self.getUrl())
        #print "url is :" + self.getUrl()
        logger.info("msg fmt is :" + self.getMsgFormat())
        #print "msg fmt is :" + self.getMsgFormat()
        logger.info("cmd type is :" + self.getCmdType())
        #print "cmd type is :" + self.getCmdType()

    def __validateMsgFmtandCmdType(self,msg_fmt,cmd_type):
        """

        :param msg_fmt:
        :param cmd_type:
        :return:
        """
        if msg_fmt == "json-rpc":
            if cmd_type == "cli" or cmd_type == "cli_ascii":
                return True
            else:
                return False
        elif msg_fmt == "xml":
            if cmd_type == "cli_show" or cmd_type == "cli_show_ascii" or cmd_type == "cli_conf":
                return True
            else:
                return False
        elif msg_fmt == "json":
            if cmd_type == "cli_show" or cmd_type == "cli_show_ascii" or cmd_type == "cli_conf":
                return True
            else:
                return False
        else:
            return False


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

    def setUrl(self,url):
        """

        :param url:
        :return:
        """
        if url == '':
            url = "http://"+ self.__swipaddrs + "/ins"
        else:
            if url.endswith("/ins"):
                self.__url = url
            elif url.endswith("/"):
                self.__url = url + "ins"
            else:
                self.__url = url + "/ins"

        self.__logInfoAbout_Url_MsgFmt_CmdType()

    def setMsgFormat_and_CmdType(self,msg_fmt='xml',cmd_type='cli_show'):
        """

        :param msg_fmt:
        :param cmd_type:
        :return:
        """
        if self.__validateMsgFmtandCmdType(msg_fmt,cmd_type):
            self.__msg_format = msg_fmt
            self.__cmd_type = cmd_type
        else:
            #TODO
            #Throw proper critical warning
            print "TODO"

        self.__logInfoAbout_Url_MsgFmt_CmdType()

    def getUrl(self):
        """

        :return:
        """
        return self.__url

    def getMsgFormat(self):
        """

        :return:
        """
        return self.__msg_format

    def getCmdType(self):
        """

        :return:
        """
        return self.__cmd_type


    def show(self,cmd):
        """

        :param cmd:
        :return:
        """

        if self.getMsgFormat() == "xml":
            myheaders = {'content-type': 'application/xml'}
            payload = """<?xml version="1.0"?>
            <ins_api>
              <version>1.2</version>
              <type>""" + self.getCmdType() + """</type>
              <chunk>0</chunk>
              <sid>sid</sid>
              <input>""" + cmd + """</input>
              <output_format>xml</output_format>
            </ins_api>"""
            response = requests.post(self.getUrl(), data=payload, headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).text

        elif self.getMsgFormat() == "json":
            myheaders = {'content-type': 'application/json'}
            payload = {
                "ins_api": {
                    "version": "1.2",
                    "type": self.getCmdType(),
                    "chunk": "0",
                    "sid": "1",
                    "input": cmd,
                    "output_format": "json"
                }
            }
            response = requests.post(self.getUrl(), data=json.dumps(payload), headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).json()

        elif self.getMsgFormat() == "json-rpc":
            myheaders = {'content-type': 'application/json-rpc'}
            payload = [
                {
                    "jsonrpc": "2.0",
                    "method": "cli",
                    "params": {
                        "cmd": "show version",
                        "version": 1.2
                    },
                    "id": 1
                }
            ]
            response = requests.post(self.getUrl(), data=json.dumps(payload), headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).json()
        return response

    def conf(self,cmd):
        """

        :param cmd:
        :return:
        """
        #TODO
        # As of now just copy pasting the same as show() method, need to find how diffrent in conf compared to show
        # Some msg fmt doesnt support conf t cmds so need to handle this, fow now it will get a response of error

        if self.getMsgFormat() == "xml":
            myheaders = {'content-type': 'application/xml'}
            payload = """<?xml version="1.0"?>
            <ins_api>
              <version>1.2</version>
              <type>""" + "cli_conf" + """</type>
              <chunk>0</chunk>
              <sid>sid</sid>
              <input>""" + cmd + """</input>
              <output_format>xml</output_format>
            </ins_api>"""
            response = requests.post(self.getUrl(), data=payload, headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).text

        elif self.getMsgFormat() == "json":
            myheaders = {'content-type': 'application/json'}
            payload = {
                "ins_api": {
                    "version": "1.2",
                    "type": "cli_conf",
                    "chunk": "0",
                    "sid": "1",
                    "input": cmd,
                    "output_format": "json"
                }
            }
            response = requests.post(self.getUrl(), data=json.dumps(payload), headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).json()

        elif self.getMsgFormat() == "json-rpc":
            myheaders = {'content-type': 'application/json-rpc'}
            payload = [
                {
                    "jsonrpc": "2.0",
                    "method": "cli",
                    "params": {
                        "cmd": "show version",
                        "version": 1.2
                    },
                    "id": 1
                }
            ]
            response = requests.post(self.getUrl(), data=json.dumps(payload), headers=myheaders,
                                     auth=(self.get_swusername_password()[0], self.get_swusername_password()[1])).json()
        return response



