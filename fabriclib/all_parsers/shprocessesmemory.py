__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowProcessesMemory(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat_for_tcam_entry = "^([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+(.*)"

        self.__data = []

        self.__process_output()

    def __process_output(self):
        for line in self.__alloutput:
            a = ""
            matchObj = re.match(self.__pat_for_tcam_entry, line.strip())
            if matchObj:
                # print line
                pid = matchObj.group(1)
                memalloc = matchObj.group(2)
                memlimit = matchObj.group(3)
                memused = matchObj.group(4)
                process = matchObj.group(5).split()[1]

                self.__data.append([pid,memalloc,memlimit,memused,process])


    def get_all_data(self):
        return tuple(self.__data)

    def get_mem_used_for_all_process(self):
        return tuple([(s[4],s[3]) for s in self.__data])
