# -*- coding: utf-8 -*-
import os
import sys
import getopt



def main(argv):
    Q = ["one_path","triangle","two_path", "rectangle"]
    Data = ["4","10","16","17","19"]
    eps = 0.1
    i = 0;
    j = 0
    try:
        opts, args = getopt.getopt(argv,"h:Q:D:e:",["QueryId=","DataId=","Epsilon="])
    except getopt.GetoptError:
        print("CollectResultsRM.py -Q <Query Id: 0(one_path)/1(triangle)/2(two_path)/3(rectangle)> -D <Data Id: 0(network4)/1(network10)/2(network16)/3(network17)/4(network19)> -e <epsilon>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("CollectResultsRM.py -Q <Query Id: 0(one_path)/1(triangle)/2(two_path)/3(rectangle)> -D <Data Id: 0(network4)/1(network10)/2(network16)/3(network17)/4(network19)> -e <epsilon>")
            sys.exit()
        elif opt in ("-Q", "--QueryId"):
            j = int(arg)
        elif opt in ("-D", "--DataId"):
            i = int(arg)
        elif opt in ("-e", "--Epsilon"):
            eps = float(arg)
    cur_path=os.getcwd()
    cmd = cur_path+"/../../dw_python "+cur_path+"/../Code/RM.py -e "+str(eps)+" -d 0.1 -I "+cur_path+"/../Information/Graph/"+Q[j]+"/network"+Data[i]+".txt"
    result = []
    time = 0
    for i in range(10):
        shell = os.popen(cmd, 'r')
        res = shell.read()
        res = res.split()
        a = float(res[2])
        b = float(res[5])
        c = float(res[7])
        result.append(abs(a-b))
        time+=c
    result.sort()
    res = sum(result)-result[0]-result[1]-result[10-1]-result[10-2]
    res = res/6
    time = time/10
    print("Error")
    print(res)
    print("Time")
    print(time)



if __name__ == "__main__":
        main(sys.argv[1:])
