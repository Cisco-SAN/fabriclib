__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowIntFcCounters(object):
    def __init__(self, output):
        self.__alloutput = output

        self.__pat_for_TimeoutDiscard = "\s+([0-9]+)\s+timeout discards.*"
        self.__TimeoutDiscard = 0

        self.__pat_for_TxWait = "\s+([0-9]+)\s+2.5us TxWait due to lack of transmit credits"
        self.__TxWait = 0

        self.__data = []

        # Call function to parse the output
        self.__process_output()

    def __process_output(self):
        for line in self.__alloutput:
            # print line
            match1 = re.match(self.__pat_for_TimeoutDiscard, line)
            if match1:
                self.__TimeoutDiscard = match1.group(1)

            match1 = re.match(self.__pat_for_TxWait, line)
            if match1:
                self.__TxWait = match1.group(1)

            self.__data.append(line)

    def get_all_data(self):
        return self.__data

    def get_TimeoutDiscard(self):
        return self.__TimeoutDiscard

    def get_TxWait(self):
        return self.__TxWait
