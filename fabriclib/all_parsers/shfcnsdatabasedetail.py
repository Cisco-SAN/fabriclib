__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowFcnsDatabaseDetail(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat_for_vsan_fcid = "^VSAN:([0-9]+)\s+FCID:(0x[0-9a-f]+)"
        self.__pat_pwwn = "port-wwn\s+\S+\s+:(\S+).*"
        self.__pat_for_da = ".*\[(.*)\]"
        self.__pat_nwwn = "node-wwn\s+:(\S+)"
        self.__pat_nodeip = "node-ip-addr\s+:(\S+)"
        self.__pat_fc4 = "fc4-types:fc4_features\s+:(\S+)"
        self.__pat_porttype = "port-type\s+:(\S+)"
        self.__pat_connint = "connected interface\s+:(\S+)"
        self.__pat_swname_swip = "switch name.*:(\S+)\s+(\S+)"

        self.__data = {}

        self.__process_output()

    def __process_output(self):
        vsan = ""
        fcid = ""
        pwwn = ""
        da = ""
        nwwn = ""
        nodeip = ""
        fc4 = ""
        porttype = ""
        connint = ""

        for line in self.__alloutput:
            matvsanfcid = re.match(self.__pat_for_vsan_fcid, line)
            matpwwn = re.match(self.__pat_pwwn, line)
            matda = re.match(self.__pat_for_da, line)
            matnwwn = re.match(self.__pat_nwwn, line)
            matnodeip = re.match(self.__pat_nodeip, line)
            matfc4 = re.match(self.__pat_fc4, line)
            matportype = re.match(self.__pat_porttype, line)
            matconnint = re.match(self.__pat_connint, line)
            matswname_ip = re.match(self.__pat_swname_swip, line)

            # pls note that order of if statements is important and 'matswname_ip' should come in the end as that the last match for a section

            if matvsanfcid:
                vsan = matvsanfcid.group(1)
                fcid = matvsanfcid.group(2)
            elif matpwwn:
                pwwn = matpwwn.group(1)
            elif matda:
                da = matda.group(1)
            elif matnwwn:
                nwwn = matnwwn.group(1)
            elif matnodeip:
                nodeip = matnodeip.group(1)
            elif matfc4:
                fc4 = matfc4.group(1)
            elif matportype:
                porttype = matportype.group(1)
            if matconnint:
                connint = matconnint.group(1)
            if matswname_ip:
                swname = matswname_ip.group(1)
                swip = matswname_ip.group(2).strip('('')')

                # End of one section so store the data
                # pwwn, index 0
                # nwwn, index 1
                # nodeip, index 2
                # fc4, index 3
                # porttype, index 4
                # connint, index 5
                # swname, index 6
                # swip, index 7
                # da, index 8
                self.__data[(vsan, fcid)] = (pwwn, nwwn, nodeip, fc4, porttype, connint, swname, swip, da)

                # Reset all the variables once data is stored
                vsan = ""
                fcid = ""
                pwwn = ""
                da = ""
                nwwn = ""
                nodeip = ""
                fc4 = ""
                porttype = ""
                connint = ""

    def get_all_data(self):
        return self.__data

    def get_all_data_by_vsan(self, vsan):
        a = [(key[1], val) for key, val in self.__data.iteritems() if str(vsan) in key]
        return dict(tuple(a))

    def get_all_data_by_fcid(self, fcid):
        a = [(key[0], val) for key, val in self.__data.iteritems() if str(fcid) in key]
        return dict(tuple(a))

    def get_local_port_and_mode_by_fcid(self, ipadd, fcid):
        retval = ""
        port_index = 5
        ip_index = 7
        for key, val in self.__data.iteritems():
            if str(fcid) in key and val[ip_index] == ipadd:
                retval = val[port_index]
                break
        return retval

    def get_nodeip_if_fc4_is_NPV(self):
        fc4_npv_index = 3
        nodeip_index = 2
        a = [val[nodeip_index] for key, val in self.__data.iteritems() if val[fc4_npv_index] == 'npv']
        return list(set(a))

    def get_connected_endports(self, ipadd):
        retval = []
        ip_index = 7
        for key, val in self.__data.iteritems():
            if val[ip_index] == ipadd:
                pwwn = val[0]
                da = val[8]
                connint = val[5]
                swip = val[7]
                retval.append([pwwn, da, connint, swip])
        return retval
