__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowInterfaceBrief(object):
    def __init__(self, output):
        self.__alloutput = output

    def get_all_output(self):
        return self.__alloutput

    def getFC_PortandOperModeasString(self):
        retval = ""
        pat1 = "^(fc[0-9]+/[0-9]+).*(trunking|up)\s+\S+\s+(\S+).*"
        # patPC = "^(port-channel[0-9]+)\s+\S+\s+\S+\s+trunking\s+TF.*"
        for line in self.__alloutput:
            matchObj = re.match(pat1, line.strip(" "))
            if matchObj:
                # print line
                port = matchObj.group(1)
                mode = matchObj.group(3)
                retval = retval + port + " " + mode + " "
            '''
            matchPC = re.match(patPC, line.strip(" "))
            if matchPC:
                port = matchPC.group(1)
                mode = 'TF'
                retval = retval+port+" "+mode+" "
            '''
        return retval
