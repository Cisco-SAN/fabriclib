__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowPortConfigInternalPortCurrCounters(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat_start_counters = "-------.*"
        self.__pat_for_each_row = "(\S+)\s+([0-9]+)"

        # example:
        # {'fcIfOutFrames': '4', 'ifOutUcastPkts': '4', 'fcIfInFrames': '4', 'ifHCOutOctets': '304', 'ifInOctets': '304', 'fcIfInOctets': '304', 'fcIfInvalidTxWords': '2', 'fcIfC3InFrames': '4', 'fcIfC3OutOctets': '304', 'ifInUcastPkts': '4', 'ifHCInOctets': '304', 'fcIfC3InOctets': '304', 'fcIfTxBBCreditTransistionToZero': '2', 'ifOutOctets': '304', 'fcIfC3OutFrames': '4', 'ifHCOutUcastPkts': '4', 'fcIfOutOctets': '304', 'ifHCInUcastPkts': '4'}
        self.__data = {}

        # Call function to parse the output
        self.__process_output()

    def __process_output(self):
        # print "Processing ..."
        start_match = False
        for line in self.__alloutput:
            # print "Line is ", line
            matchstart = re.match(self.__pat_start_counters, str(line).strip())
            if matchstart:
                start_match = True
            matchrow = re.match(self.__pat_for_each_row, str(line).strip())
            if matchrow and start_match:
                self.__data[matchrow.group(1)] = matchrow.group(2)

    def get_all_data(self):
        return self.__data
