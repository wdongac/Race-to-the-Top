#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random
import cplex
import numpy as np
import time



def ReadInput():
    global input_file_path
    global tuples
    global connections
    global downward_sensitivity
    size_dic = {}
    id_dic = {}
    id_num = 0
    #Collect the DS
    downward_sensitivity = 0
    
    #The variable is repsented one entity
    #We use connection to show the connections between entity and query results
    tuples = []
    connections = []
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        connection = []
        for element in elements:
            element = int(element)
            #Re-order the IDs
            if element in id_dic.keys():
                element = id_dic[element]
            else:
                tuples.append(id_num)
                id_dic[element] = id_num
                element = id_num
                id_num+=1                
            if element in size_dic.keys():
                size_dic[element]+=1
            else:
                size_dic[element] = 1
            if downward_sensitivity<=size_dic[element]:
                downward_sensitivity = size_dic[element];                
            connection.append(element)
        connections.append(connection)
      
        

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
    global downward_sensitivity
    global connections
    num_connections = len(connections)
    base = math.e
    max_i = int(math.log(global_sensitivity,base))+1
    res = []
    for i in range(1,max_i+1):
        tau = math.pow(base,i)
        t_res = 0
        if tau>=downward_sensitivity:
            t_res = num_connections
        else:   
            t_res = LPSolver(tau)
        res.append(t_res+LapNoise()*tau/epsilon*max_i-tau/epsilon*max_i*math.log(max_i/beta,math.e))
    max_ind = 1
    max_val = 0
    for i in range(1,max_i+1):
        if res[i-1]>max_val:
            max_val = res[i-1]
            max_ind = i
    tau = math.pow(base,max_ind)
    final_res = max_val+tau/epsilon*max_i*math.log(max_i/beta,math.e)
    print(tau)
    return final_res

      

def LPSolver(tau):
    global tuples
    global connections
    num_constraints = len(tuples)
    num_variables = len(connections)
    
    # Set the obj
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.maximize)

    #Set variables
    obj = np.ones(num_variables)
    ub = np.ones(num_variables)
    cpx.variables.add(obj=obj, ub=ub)
    
    #Set the right hand side and the sign
    rhs = np.ones(num_constraints)*tau
    senses = "L" * num_constraints
    cpx.linear_constraints.add(rhs=rhs, senses=senses)
    
    #Set the coefficients
    cols = []
    rows = []
    vals = []
    
    for i in range(num_variables):
        for j in connections[i]:
            cols.append(i)
            rows.append(j)
            vals.append(1)
    cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
    cpx.solve()
    return cpx.solution.get_objective_value()
        


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
    start = time.time()
    ReadInput()
    res = RunAlgorithm()
    end= time.time()
    print(res)
    print(end-start)
    
	

if __name__ == "__main__":
	main(sys.argv[1:])