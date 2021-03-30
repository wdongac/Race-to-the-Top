#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random



def ReadInput():
    global input_file_path
    global size_dic
    size_dic = {}
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        element = elements[0]
        if element in size_dic.keys():
            size_dic[element]+=1
        else:
            size_dic[element] = 1
    
    
    
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
    base = math.e
    max_i = int(math.log(global_sensitivity,base))+1
    res = []
    for i in range(1,max_i+1):
        tau = math.pow(math.e,i)
        res.append(LP(tau)+LapNoise()*math.pow(base,i)/epsilon*max_i-math.pow(base,i)/epsilon*max_i*math.log(max_i/beta,math.e))
    return max(res)
    
    

def LP(tau):
    global size_dic
    res = 0
    for element in size_dic.keys():
        res += min(tau,size_dic[element])
    return res



def main(argv):
    global input_file_path
    global epsilon
    global beta
    global global_sensitivity
	
    try:
        opts, args = getopt.getopt(argv,"h:I:e:b:G:",["Input=","epsilon=","beta=","GlobalSensitivity="])
    except getopt.GetoptError:
        print("OurMechanismSJF.py -I <input file> -e <epsilon> -b <beta> -G <global sensitivity>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("OurMechanismSJF.py -I <input file> -e <epsilon> -b <beta> -G <global sensitivity>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = str(arg)
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
    ReadInput()
    res = RunAlgorithm()
    print(res)
    
	

if __name__ == "__main__":
	main(sys.argv[1:])
