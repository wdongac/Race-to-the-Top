#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import multiprocessing
manager = multiprocessing.Manager()



def main(argv):
    repeat_time = 10
    threads_num = 5
    global S
    global Q
    global GS
    global SJ
    global queries
    global times
    global results
    cur_path=os.getcwd()
    S = manager.list()
    Q = manager.list()
    GS = manager.list()
    SJ = manager.list()
    Q = [5,8,21,3,12,20,10,7,11,18]
    Q = [5]
    S = ["3"]
    GS = [100000,1000000,1000000,1000000,1000000,1000000,1000000,100000000,1000000,100000000]
    for i in range(len(GS)):
        GS[i] = GS[i]/8
    SJ = [1,1,1,0,0,0,0,1,0,0]
    queries = manager.list()
    times = manager.list()
    results = manager.list()
    for i in range(len(S)):
        time_i = manager.list()
        result_i = manager.list()
        query_i = manager.list()
        for j in range(len(Q)):
            time_i_j = manager.list()
            result_i_j = manager.list()
            for k in range(8):
                time_i_j_k = 0.0
                result_i_j_k = manager.list()
                time_i_j.append(time_i_j_k)
                result_i_j.append(result_i_j_k)
            time_i.append(time_i_j)
            result_i.append(result_i_j)
            query_i.append(0)
        times.append(time_i)
        results.append(result_i)
        queries.append(query_i)
    #Assign works to threads
    assigned_i = []
    assigned_j = []
    assigned_k = []
    for i in range(threads_num):
        assigned_i.append([])
        assigned_j.append([])
        assigned_k.append([])
    start_id = 0
    for i in range(len(S)):
        for j in range(len(Q)):
            for k in range(8):
                for f in range(repeat_time):
                    assigned_i[start_id].append(i)
                    assigned_j[start_id].append(j)
                    assigned_k[start_id].append(k)
                    start_id = (start_id+1)%threads_num
    threads = []
    for i in range(threads_num):
        threads.append(multiprocessing.Process(target=ThreadWork,args=(i,assigned_i[i],assigned_j[i],assigned_k[i],cur_path)))
    for i in range(threads_num):
        threads[i].start()
    for i in range(threads_num):
        threads[i].join()
    for i in range(len(S)):
        for j in range(len(Q)):
            output_file = cur_path+"/../Result/TPCH/R2T_"+str(Q[j])+".txt"
            output = open(output_file, 'w')
            for k in range(8):
                print(str(i)+" "+str(j)+" "+str(k))
                times[i][j][k] /= repeat_time
                results[i][j][k].sort()
                res = sum(results[i][j][k])-results[i][j][k][0]-results[i][j][k][1]-results[i][j][k][repeat_time-1]-results[i][j][k][repeat_time-2]
                res = res/(repeat_time-4)
                output.write(str(pow(2,k))+" "+str(queries[i][j])+" "+str(res)+" "+str(times[i][j][k])+"\n")
                
                
      
def ThreadWork(thread_id,assigned_i,assigned_j,assigned_k,cur_path):
    global S
    global Q
    global GS
    global SJ
    global queries
    global times
    global results
    work_num = len(assigned_i)
    for l in range(work_num):
        i = assigned_i[l]
        j = assigned_j[l]
        k = assigned_k[l]
        print(str(i)+" "+str(j)+" "+str(k))
        #Create a new file
        cmd = "cp "+cur_path+"/../Information/TPCH/Q"+str(Q[j])+"_"+S[i]+".txt "+cur_path+"/../Temp/Q"+str(Q[j])+"_"+str(thread_id)+".txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()
        #Collect the result for algorithm
        cmd = cur_path+"/../../dw_python "+cur_path+"/../Code/R2T"
        if SJ[j]==0:
            cmd = cmd+"SJF"
        cmd = cmd+".py -I "+cur_path+"/../Temp/Q"+str(Q[j])+"_"+str(thread_id)+".txt"
        cmd = cmd+" -b 0.1 -e "+str(pow(2,k)*0.1)+" -G "+str(GS[j]*pow(2,i+3))
        if SJ[j]==1:
            cmd = cmd+" -p 10"
        shell = os.popen(cmd, 'r')
        res = shell.read()
        res = res.split()
        a = float(res[2])
        b = float(res[5])
        c = float(res[7])
        results[i][j][k].append(abs(a-b))        
        queries[i][j] = a
        times[i][j][k] = times[i][j][k]+c
        shell.close()
        #Remove the new file
        cmd = "rm "+cur_path+"/../Temp/Q"+str(Q[j])+"_"+str(thread_id)+".txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()                 
    
   
                
if __name__ == "__main__":
	main(sys.argv[1:])