__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowHardIntStatsDevFcMacAllPort(object):
    def __init__(self, output):
        self.__alloutput = output

        self.__pat_for_TxBBZ = "[0-9]+.*TBBZ\S+\s+([0-9]+)\s+.*"
        self.__TxBBZ = 0

        self.__pat_for_RxBBZ = "[0-9]+.*RBBZ\S+\s+([0-9]+)\s+.*"
        self.__RxBBZ = 0

        self.__data = []

        # Call function to parse the output
        self.__process_output()

    def __process_output(self):
        for line in self.__alloutput:
            # print line
            match1 = re.match(self.__pat_for_TxBBZ, line)
            if match1:
                self.__TxBBZ = match1.group(1).lstrip('0')

            match1 = re.match(self.__pat_for_RxBBZ, line)
            if match1:
                self.__RxBBZ = match1.group(1).lstrip('0')

            self.__data.append(line)

    def get_all_data(self):
        return self.__data

    def get_TxBBZ(self):
        return self.__TxBBZ

    def get_RxBBZ(self):
        return self.__RxBBZ
