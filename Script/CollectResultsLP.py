# -*- coding: utf-8 -*-
import sys
import os



def Process(i,j, cur_path):
    global Q
    global max_degree
    global q_pow
    global Data
    input_file_path = cur_path+"/../Result/Graph/LP_All_Tau_"+str(Q[j])+"_network"+Data[i]+".txt"
    input_file = open(input_file_path, 'r')
    output_file = cur_path+"/../Result/Graph/LP_"+str(Q[j])+"_network"+Data[i]+".txt"
    output = open(output_file, 'w')
    lines = input_file.readlines()
    GS = pow(max_degree[i],q_pow[j])
    tau = 2
    ii = 0
    times = []
    err = []
    sort_err = []
    for k in range(8):
        times.append([])
        err.append([])
        sort_err.append([])
    num_line = len(lines)
    q_res = 0
    while(tau<=GS):
        if ii*11+6>num_line:
            tau*=2
            ii+=1
            for k in range(8):
                err[k].append(10000000000000)
                times[k].append(10000000000000)
                sort_err[k].append(10000000000000)
            continue
        l1 = lines[ii*11+1]
        l3 = lines[ii*11+2]
        for k in range(8):
            elements = l3.split()
            q_res = float(elements[2])
            l2 = lines[ii*11+3+k]
            elements = l1.split()
            times[k].append(float(elements[1]))
            elements = l2.split()
            err[k].append(float(elements[1]))
            sort_err[k].append(float(elements[1]))
        tau*=2
        ii+=1
    for k in range(8):
        sort_err[k].sort()
        middle_id = int(len(err[k])/2)
        middle_err = sort_err[k][middle_id]
        middle_time = -1
        for ii in range(len(err[k])):
            if err[k][ii]==middle_err:
                middle_time = times[k][ii]
        output.write(str(pow(2,k)*0.1)+" "+str(q_res)+" "+str(middle_err)+" "+str(middle_time)+"\n")
    
    
    
def main(argv):
    global Q
    global max_degree
    global q_pow
    global Data
    cur_path=os.getcwd()
    Q = ["one_path","triangle","two_path", "rectangle"]
    Data = ["4","10","16","17","19"]
    max_degree = [1024,512,16,16,512]
    q_pow = [1,2,2,3]
    for i in range(len(Data)):
        for j in range(len(Q)):
            Process(i,j, cur_path)
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])

