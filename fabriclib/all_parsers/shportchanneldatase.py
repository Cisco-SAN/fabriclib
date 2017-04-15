__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowPortChannelDatabase(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat = "^(port-cha.*)"
        self.__patfirstoper = "First operational port is (.*)"
        self.__pat_ports = ".*(fc[0-9]+/[0-9]+)\s+\[(.*)\].*"
        self.__pc_ports = {}
        self.__pc_first_oper_port = {}

        self.__process_output()

    def __process_output(self):
        pc = ""
        p_list = []
        for line in self.__alloutput:
            # print line.strip(" ")

            matchObj = re.match(self.__pat, line.strip(" "))
            if matchObj:
                # print "match"
                if pc != "":
                    # print pc
                    # print p_list
                    self.__pc_ports[pc] = p_list
                    p_list = []
                    # print self.__pc_ports
                pc = matchObj.group(1).strip('\r\n\t')

            match_fo = re.match(self.__patfirstoper, line.strip(" "))
            if match_fo:
                # print "matchfo"
                self.__pc_first_oper_port[pc] = match_fo.group(1).strip()

            match_ports = re.match(self.__pat_ports, line.strip(" "))
            if match_ports:
                # print "match ports"
                p_list.append([match_ports.group(1), match_ports.group(2)])

    def get_all_pc(self):
        pclist = []
        for key, val in self.__pc_ports.iteritems():
            pclist.append(key)
        return pclist

    def get_pc_ports(self, pc):
        # print "pc is" + pc
        # print self.__pc_ports
        return self.__pc_ports[pc]
