#!/usr/bin/env python3

import re
from datetime import datetime
from collections import Counter
import pprint


# 1. Of all the `Poisoned` responses logged, how many queries of each MNR protocol were sent during
# the time Responder was running?
def task1(file_name):
    mdns = 0
    llmnr = 0
    nbtns = 0

    with open(file_name, 'r') as log:
        for line in log.readlines():
            if "[MDNS]" in line:
                mdns += 1
            elif "[LLMNR]" in line:
                llmnr += 1
            elif "[NBT-NS]" in line:
                nbtns += 1

    print('-' * 25, "Task 1 Solutions:", '-' * 25)
    print("MDNS total:", mdns, "\nLLMNR total:", llmnr, "\nNBT-NS total:", nbtns)
    # print("Total:", mdns+llmnr+nbtns) - prints the total of the protocols found


# 2. Of the `Poisoned` responses logged, what are the 10 most common hosts
# (i.e. hashes of the hostname)?
def task2(file_name):
    host_dict = {}

    with open(file_name, 'r') as log:
        for line in log.readlines():
            line = line.strip()
            line = re.split('Poisoned answer sent to | for name ', line)
            if len(line) == 3:
                if line[1] in host_dict:
                    host_dict[line[1]] += 1
                else:
                    host_dict[line[1]] = 1

        common_hashes = Counter(host_dict).most_common(10)

        print('\n' + '-' * 25, "Task 2 Solutions:", '-' * 25)
        print(' ' * 25, "Most common hosts", ' ' * 22, "Number of times seen")
        for i in common_hashes:
            print(i[0], "|", i[1])
        #pprint.pprint(hashDict) --- prints the entire dictionary nicely
        #print(sum(hashDict.values())) --- prints the sum of all the values in the dictionary


# 3. Of the `Poisoned` responses logged, what are the 10 most common queries?
def task3(file_name):
    query_dict = {}

    with open(file_name, 'r') as log:
        for line in log.readlines():
            line = line.strip()
            line = re.split('Poisoned answer sent to | for name | \(', line)
            if len(line) == 3 or len(line) == 4:
                if line[2] in query_dict:
                    query_dict[line[2]] += 1
                else:
                    query_dict[line[2]] = 1

        common_queries = Counter(query_dict).most_common(10)

        print('\n' + '-' * 25, "Task 3 Solutions:", '-' * 25)
        print(' ' * 25, "Most common queries", ' ' * 20, "Number of times seen")
        for i in common_queries:
            print(i[0], "|", i[1])
        #pprint.pprint(hashDict) --- prints the entire dictionary nicely
        #print(sum(hashDict.values())) --- prints the sum of all the values in the dictionary


'''
4. A NTLM version 1 hash was leaked to Responder (i.e. Responder tricked the
   victim machine into giving it the hash) as part of an attempt by a host to
   log into a `MSSQL` instance. There is a `Client`, `Hash`, and `Username`
   associated with these leaked credentials.

   What is the `Client` that sent those credentials?

   How many times was a `Poisoned` response sent to that host?
'''
def task4(file_name):
    with open(file_name, 'r') as log:
        for line in log.readlines():
            if "NTLM" in line:
                #print(line) --- each of the NTLM user, hash, and client lines from the log
                if "Client:" in line:
                    line=line.split("Client: ")
                    client = line[1].strip()

    poisoned_responses = 0

    with open(file_name, 'r') as log:
        for line in log.readlines():
            if client in line and "Poisoned" in line:
                poisoned_responses += 1
                #print(line) --- The poisoned responses sent from the log

        print('\n' + '-' * 25, "Task 4 Solutions:", '-' * 25)
        print("Client:", client)
        print("Number of poisoned responses sent:", poisoned_responses)


# 5. When was Responder started? When did it end?
def task5(file_name):
    times = []

    with open(file_name, 'r') as log:
        for line in log.readlines():
            line = re.split('-', line)
            times.append(datetime.strptime(line[0], "%m/%d/%Y %H:%M:%S %p "))

        print('\n' + '-' * 25, "Task 5 Solutions:", '-' * 25)
        print("Start:", min(times))
        print("End:", max(times))
        #print(len(dt)) --- number of entries in the list

def main():
    file_name = "responder.log"

    task1(file_name)
    task2(file_name)
    task3(file_name)
    task4(file_name)
    task5(file_name)

if __name__ == '__main__':
    main()
