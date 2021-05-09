# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random
import time



def ReadInput():
    global input_file_path
    global size_dic
    size_dic = {}
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        value = float(elements[0])
        entity = int(elements[0])
        if entity in size_dic.keys():
            size_dic[entity] += value
        else:
            size_dic[entity] = value
    
    
    
def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c>0.5:
        return b
    else:
        return -b
    


def RunAlgorithm():
    global global_sensitivity
    global beta
    base = math.e
    max_i = int(math.log(global_sensitivity,base))+1
    max_res1 = -10000000
    max_res2 = 0
    for i in range(1,max_i+1):
        tau = math.pow(math.e,i)
        t_res2 = LP(tau)+LapNoise()*math.pow(base,i)/epsilon*max_i
        t_res1 = t_res2 - math.pow(base,i)/epsilon*max_i*math.log(max_i/beta,math.e)
        if t_res1>max_res1:
            max_res1 = t_res1
            max_res2 = t_res2
    return max_res2
    
    

def LP(tau):
    global size_dic
    res = 0
    for element in size_dic.keys():
        res += min(tau,size_dic[element])
    return res



def main(argv):
    #The input file including the relationships between aggregations and base tuples
    global input_file_path
    input_file_path = ""
    #Privacy budget
    global epsilon
    epsilon = 0.1
    #Error probablity: with probablity at least 1-beta, the error can be bounded
    global beta
    beta = 0.01
    #The global sensitivity
    global global_sensitivity
    global_sensitivity = 1000000
    try:
        opts, args = getopt.getopt(argv,"h:I:e:b:G:",["Input=","epsilon=","beta=","GlobalSensitivity="])
    except getopt.GetoptError:
        print("DPAggreSJF.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.01)> -G <global sensitivity(default 1000,000)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("DPAggreSJF.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.01)> -G <global sensitivity(default 1000,000)")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = str(arg)
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
    start = time.time()
    ReadInput()
    res = RunAlgorithm()
    end= time.time()
    print("Result")
    print(res)
    print("Time")
    print(end-start)
    
	

if __name__ == "__main__":
	main(sys.argv[1:])
