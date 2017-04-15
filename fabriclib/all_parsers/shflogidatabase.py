__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowFlogiDatabase(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat = "^(fc[0-9]+/[0-9]+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+).*"

        self.__data = []

        self.__process_output()

    def __process_output(self):
        for line in self.__alloutput:
            matchObj = re.match(self.__pat, line.strip(" "))
            if matchObj:
                # print line
                port = matchObj.group(1)
                vsan = matchObj.group(2)
                fcid = matchObj.group(3)
                pwwn = matchObj.group(4)
                nwwn = matchObj.group(5)
                self.__data.append((port, vsan, fcid, pwwn, nwwn))

    def get_all_flogi_details(self):
        return tuple(self.__data)

    def get_all_flogi_int_fcid_details(self):
        # get all (int,fcid) details as tuple of tuples
        return tuple([(s[0], s[2]) for s in self.__data])
